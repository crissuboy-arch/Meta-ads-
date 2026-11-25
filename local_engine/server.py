"""Servidor HTTP minimo do motor local (Modo Local) - loopback apenas,
nunca expoe a porta publicamente. Chamado pelo sidecar do Tauri
(src-tauri/src/main.rs), roda inteiro no computador do proprio comprador.

De proposito sem dependencias pesadas nesta primeira versao, para nao
exigir empacotar um runtime extra agora - ver docs/motor-local.md para o
que falta para distribuicao comercial (empacotar o proprio Python em vez
de depender do Python do sistema do comprador).
"""
import json
import os
import sys
import secrets
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_engine import engine  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    def _authorize(self):
        token = getattr(self.server, "auth_token", "")
        if self.headers.get("Origin") or not token or not hmac.compare_digest(
                self.headers.get("Authorization", ""), "Bearer " + token):
            self._json(403, {"ok": False, "error": "local_engine_access_denied"})
            return False
        return True

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length < 0 or length > 1048576:
            raise ValueError("payload_too_large")
        if self.headers.get_content_type() != "application/json":
            raise ValueError("json_required")
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return {}

    def log_message(self, fmt, *args):
        pass  # roda local, sem necessidade de log de acesso em stdout

    def do_GET(self):
        if not self._authorize():
            return
        path = urlsplit(self.path).path
        if path == "/health":
            return self._json(200, {"ok": True})
        if path == "/agents":
            q = parse_qs(urlsplit(self.path).query)
            lang = (q.get("lang") or ["pt"])[0]
            return self._json(200, {"agents": engine.load_agents(lang=lang)})
        if path == "/providers/detect":
            return self._json(200, engine.detect_clis())
        self._json(404, {"error": "not_found"})

    def do_POST(self):
        if not self._authorize():
            return
        path = urlsplit(self.path).path
        try:
            body = self._body()
            if not isinstance(body, dict):
                raise ValueError("object_required")
        except (ValueError, TypeError) as exc:
            return self._json(400, {"ok": False, "error": str(exc)})
        parts = [p for p in path.split("/") if p]
        if len(parts) == 3 and parts[0] == "providers" and parts[2] == "terminal":
            return self._json(200, engine.open_provider_terminal(parts[1]))
        if path == "/infer/cli":
            out = engine.run_cli_inference(
                body.get("provider", ""), body.get("system_prompt", ""), body.get("text", ""))
            return self._json(200 if out.get("ok") else 400, out)
        if path == "/chat":
            out = engine.chat(body.get("provider", ""), body.get("module", ""),
                              body.get("messages", []), body.get("lang", "pt"),
                              body.get("context"))
            return self._json(200 if out.get("ok") else 400, out)
        if path == "/infer/byok":
            out = engine.byok_call(
                body.get("provider", ""), body.get("api_key", ""),
                body.get("system_prompt", ""), body.get("text", ""), model=body.get("model"))
            return self._json(200 if out.get("ok") else 400, out)
        if path == "/mcp/call":
            out = engine.mcp_relay(
                body.get("base_url", ""), body.get("key", ""),
                body.get("tool", ""), body.get("args") or {})
            return self._json(200 if out.get("ok") else 400, out)
        self._json(404, {"error": "not_found"})


def main():
    port = int(os.environ.get("LOCAL_ENGINE_PORT", "0"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.auth_token = secrets.token_urlsafe(32)
    # Imprime a porta real escolhida (util quando port=0) para o processo
    # pai (Tauri/Rust) saber onde falar com o motor.
    print("LOCAL_ENGINE_READY=" + json.dumps({"port": server.server_address[1],
                                              "token": server.auth_token}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
