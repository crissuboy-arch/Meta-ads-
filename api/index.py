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

from app_core import create_app

_fastapi_app = create_app()

# On Vercel, the catch-all rewrite in vercel.json routes every request to this
# function, and the app receives the *rewritten* path ("/api/index", or
# "/api/index" + the original path) instead of the path the visitor asked for.
# FastAPI then answers 404 {"detail":"Not Found"} even for "/". Strip that
# prefix before dispatching so the real routes match. Local runs (server.py)
# don't go through this file and are unaffected.
_PREFIXES = ("/api/index.py", "/api/index")


async def app(scope, receive, send):
    if scope.get("type") in ("http", "websocket"):
        path = scope.get("path") or ""
        for prefix in _PREFIXES:
            if path == prefix:
                scope = {**scope, "path": "/", "raw_path": b"/"}
                break
            if path.startswith(prefix + "/"):
                stripped = path[len(prefix):]
                scope = {
                    **scope,
                    "path": stripped,
                    "raw_path": stripped.encode("utf-8"),
                }
                break
    await _fastapi_app(scope, receive, send)
