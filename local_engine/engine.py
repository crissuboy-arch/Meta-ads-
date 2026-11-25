"""Motor local independente (Modo Local) - Fase III/IV.

Roda no computador do proprio comprador (nunca na Vercel compartilhada),
chamado pelo sidecar do Tauri (src-tauri/src/main.rs). Responsabilidades:

1. Detectar CLIs oficiais ja instaladas (claude/codex/opencode) e abrir um
   terminal autenticado para cada uma - a mesma experiencia validada nesta
   conversa com o OpenBot: o motor NUNCA pede nem guarda login/senha, so
   abre o terminal onde a propria CLI oficial cuida do OAuth dela.
2. Rodar inferencia usando a CLI ja autenticada pelo usuario (sem chave de
   API), OU usando BYOK (chave de API propria) como alternativa - secao 3
   do pedido.
3. Repassar chamadas de dados reais do Meta Ads para o conector MCP remoto
   QUE JA EXISTE na plataforma hospedada (/mcp/{key}, mesma tela "Conectar
   Claude"), reaproveitando a trava de escrita corrigida na Fase I em vez
   de reimplementar OAuth do Meta/Graph API localmente.

Ver docs/motor-local.md para o que esta confirmado por teste automatizado
vs. o que precisa de confirmacao manual do proprio usuario (comandos
exatos de codex/opencode nao instalados neste ambiente de desenvolvimento).
"""
import json
import os
import platform
import shutil
import subprocess
import urllib.error
import urllib.request

AGENT_IDS = [
    "coordenador-marketing-ia",
    "gestor-trafego-pago",
    "analista-financeiro",
    "auditor-campanhas",
    "especialista-pixel-rastreamento",
    "especialista-copy-criativos",
    "pesquisador-mercado",
    "especialista-funis-ofertas",
    "mentor-trafego-pago",
    "gestor-mentor-trafego",
]

CLI_PROVIDERS = ["claude", "codex", "opencode"]

# Mesmas ferramentas de escrita protegidas por WRITE_ACTIONS_ENABLED no app
# hospedado (ads_connect.py, corrigido na Fase I) - o motor local nunca as
# chama sem aprovacao humana explicita, por cima da trava do servidor.
WRITE_TOOLS = {"create_campaign", "create_adset", "create_ad", "set_status"}


def _config_path(lang="pt"):
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    name = "meta-ads.json" if lang == "en" else f"meta-ads-{lang}.json"
    return os.path.join(root, "configs", name)


def load_agents(lang="pt"):
    """Le id/prompt dos agentes direto de configs/meta-ads*.json - mesma
    fonte de verdade portada na Fase II, sem duplicar texto num segundo
    lugar que poderia divergir."""
    with open(_config_path(lang), encoding="utf-8") as f:
        cfg = json.load(f)
    tools_by_id = {t["id"]: t for t in cfg.get("tools", [])}
    prompts = cfg.get("prompts", {})
    agents = []
    for agent_id in AGENT_IDS:
        tool = tools_by_id.get(agent_id)
        prompt = prompts.get(agent_id)
        if not tool or not prompt:
            continue
        agents.append({
            "id": agent_id,
            "icon": tool.get("icon", ""),
            "label": tool.get("label", agent_id),
            "desc": tool.get("desc", ""),
            "system_prompt": prompt,
        })
    return agents


def detect_clis(which=shutil.which):
    """Deteccao real via PATH - nunca assume, so reporta o que encontra."""
    return {name: bool(which(name)) for name in CLI_PROVIDERS}


# Comando nao-interativo de cada CLI oficial para obter uma resposta de
# texto. O de `claude` e documentado oficialmente (`claude -p`); os de
# `codex`/`opencode` sao o melhor entendimento a partir da documentacao
# publica consultada nesta conversa, mas nao foram executados de verdade
# neste ambiente (CLIs nao instalados aqui) - CONFIRMAR MANUALMENTE antes
# de depender deles em produção (ver docs/motor-local.md).
CLI_EXEC = {
    "claude": lambda prompt: ["claude", "-p", prompt, "--max-turns", "1"],
    "codex": lambda prompt: ["codex", "exec", "--skip-git-repo-check", prompt],
    "opencode": lambda prompt: ["opencode", "run", prompt],
}


def run_cli_inference(provider, system_prompt, user_text, timeout=60,
                       runner=subprocess.run, which=shutil.which):
    """Usa a CLI oficial ja autenticada pelo PROPRIO usuario como motor de
    inferencia - nenhuma chave de API, nenhum login armazenado aqui."""
    if provider not in CLI_EXEC:
        return {"ok": False, "error": f"provedor desconhecido: {provider}"}
    if not which(provider):
        return {"ok": False, "error": f"{provider} nao esta instalado/no PATH"}
    full_prompt = f"{system_prompt}\n\n{user_text}" if system_prompt else user_text
    cmd = CLI_EXEC[provider](full_prompt)
    try:
        proc = runner(cmd, capture_output=True, text=True, timeout=timeout)
    except Exception as exc:
        return {"ok": False, "error": f"falha ao executar {provider}: {exc}"}
    if proc.returncode != 0:
        return {"ok": False, "error": (proc.stderr or proc.stdout or "erro desconhecido")[:500]}
    return {"ok": True, "text": (proc.stdout or "").strip()}


TERMINAL_CMD = {
    "Windows": lambda bin_: ["cmd", "/c", "start", "cmd", "/k", bin_],
    "Darwin": lambda bin_: ["osascript", "-e",
                             f'tell application "Terminal" to do script "{bin_}"'],
    "Linux": lambda bin_: ["x-terminal-emulator", "-e", bin_],
}


def open_provider_terminal(provider, system=platform.system,
                            popen=subprocess.Popen, which=shutil.which):
    """Abre um terminal rodando a CLI oficial pura (sem argumentos) para o
    usuario autenticar do jeito nativo dela - mesma logica validada com o
    OpenBot nesta conversa: o app nunca pede email/senha/codigo."""
    if provider not in CLI_PROVIDERS:
        return {"ok": False, "error": f"provedor desconhecido: {provider}"}
    if not which(provider):
        return {"ok": False,
                 "error": f"{provider} nao esta instalado/no PATH. Instale o CLI oficial primeiro."}
    os_name = system()
    builder = TERMINAL_CMD.get(os_name)
    if not builder:
        return {"ok": False, "error": f"sistema operacional nao suportado: {os_name}"}
    try:
        popen(builder(provider))
    except Exception as exc:
        return {"ok": False, "error": f"falha ao abrir terminal: {exc}"}
    return {"ok": True}


def mcp_relay(base_url, key, tool_name, args, approved=False,
              opener=urllib.request.urlopen):
    """Chama o conector MCP remoto QUE JA EXISTE na plataforma hospedada
    (/mcp/{key}, o mesmo da tela 'Conectar Claude'), reaproveitando 100% a
    logica e a trava de escrita corrigida na Fase I - o motor local nao
    reimplementa OAuth do Meta nem a Graph API.
    """
    if tool_name in WRITE_TOOLS and not approved:
        return {"ok": False,
                 "error": "acao de escrita exige aprovacao humana explicita (approved=true)"}
    url = base_url.rstrip("/") + "/mcp/" + key
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": tool_name, "arguments": args or {}},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload,
                                  headers={"Content-Type": "application/json"})
    try:
        with opener(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return {"ok": False, "error": f"falha ao falar com {url}: {exc}"}
    result = body.get("result") or {}
    if result.get("isError"):
        return {"ok": False, "error": (result.get("content") or [{}])[0].get("text", "erro MCP")}
    text = (result.get("content") or [{}])[0].get("text", "")
    return {"ok": True, "text": text}


BYOK_DEFAULT_MODEL = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-sonnet-4-5",
    "gemini": "gemini-2.0-flash",
    "openrouter": "openai/gpt-4o-mini",
}


def byok_call(provider, api_key, system_prompt, user_text, model=None,
              opener=urllib.request.urlopen):
    """Alternativa sem CLI (secao 3 do pedido): mesmo formato de chamada ja
    usado/testado em app_core._prov_text, para o motor local nao inventar
    um segundo jeito de falar com os mesmos provedores."""
    model = model or BYOK_DEFAULT_MODEL.get(provider)
    if provider == "anthropic":
        url = "https://api.anthropic.com/v1/messages"
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01",
                   "Content-Type": "application/json"}
        payload = {"model": model, "max_tokens": 1500,
                   "system": system_prompt or "",
                   "messages": [{"role": "user", "content": user_text}]}

        def parse(d):
            return "".join(p.get("text", "") for p in d.get("content", [])
                            if p.get("type") == "text")
    elif provider in ("openai", "openrouter"):
        url = ("https://api.openai.com/v1/chat/completions" if provider == "openai"
               else "https://openrouter.ai/api/v1/chat/completions")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        msgs = ([{"role": "system", "content": system_prompt}] if system_prompt else [])
        msgs.append({"role": "user", "content": user_text})
        payload = {"model": model, "messages": msgs}

        def parse(d):
            return (d.get("choices") or [{}])[0].get("message", {}).get("content", "")
    elif provider == "gemini":
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/{model}:"
               f"generateContent?key={api_key}")
        headers = {"Content-Type": "application/json"}
        text = (system_prompt + "\n\n" + user_text) if system_prompt else user_text
        payload = {"contents": [{"parts": [{"text": text}]}]}

        def parse(d):
            parts = (d.get("candidates") or [{}])[0].get("content", {}).get("parts", [])
            return "".join(p.get("text", "") for p in parts)
    else:
        return {"ok": False, "error": f"provedor desconhecido: {provider}"}

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                  headers=headers)
    try:
        with opener(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return {"ok": False, "error": f"falha ao chamar {provider}: {exc}"}
    try:
        text = parse(data)
    except Exception:
        text = ""
    if not text:
        return {"ok": False, "error": f"{provider} nao retornou texto"}
    return {"ok": True, "text": text}
