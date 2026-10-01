import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

configs_dir = _root / "configs"
if not configs_dir.is_dir():
    raise RuntimeError(
        f"Diretorio 'configs/' nao encontrado em {configs_dir}. "
        "Verifique se o deploy inclui todos os arquivos."
    )

import json

# TEMPORARY PROBE (deploy diagnostic): answer every HTTP request with the raw
# ASGI routing info Vercel hands us, so we can see the exact path/root_path the
# function receives behind the vercel.json catch-all rewrite. Remove after use.
async def app(scope, receive, send):
    if scope.get("type") == "lifespan":
        while True:
            msg = await receive()
            if msg["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif msg["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
    if scope.get("type") != "http":
        return
    body = json.dumps(
        {
            "path": scope.get("path"),
            "raw_path": (scope.get("raw_path") or b"").decode("utf-8", "replace"),
            "root_path": scope.get("root_path"),
            "method": scope.get("method"),
            "query_string": (scope.get("query_string") or b"").decode(
                "utf-8", "replace"
            ),
        }
    ).encode()
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(body)).encode()],
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})
