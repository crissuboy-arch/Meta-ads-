import base64
import json
import os
import re
import tempfile
import time
import urllib.parse
from pathlib import Path

from config import (
    CONFIG,
    MODELS as APP_MODELS,
    get_config,
    get_lang_config,
    list_configs,
    normalize_lang,
    reload_config,
    PLATFORM_PATTERNS,
    PRODUCT_TYPE_KEYWORDS,
    SYSTEM_PROMPTS,
    UPLOADS,
)

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from openai import OpenAI

try:
    import requests as _requests
except ImportError:
    _requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

BASE_URL = "https://integrate.api.nvidia.com/v1"
DEFAULT_MODEL = APP_MODELS.get("default", "meta/llama-3.1-70b-instruct")
REQUEST_TIMEOUT = 60

# ---------------------------------------------------------------------------
# AI providers (all OpenAI-compatible). Add a provider by dropping its key in
# the .env / Vercel env vars; models register only when their key exists.
#   nvidia     -> NVIDIA_API_KEY      (free key at build.nvidia.com)
#   openrouter -> OPENROUTER_API_KEY  (free :free models at openrouter.ai)
#   agnes      -> AGNES_API_KEY       (Agnes AI free tier, apihub.agnes-ai.com)
# ---------------------------------------------------------------------------
API_PROVIDERS = {
    "nvidia": {
        "label": "NVIDIA NIM (free)",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "key_env": "NVIDIA_API_KEY",
        "headers": {},
    },
    "openrouter": {
        "label": "OpenRouter",
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "headers": {"X-Title": "Meta Ads Expert PRO"},
    },
    "agnes": {
        "label": "Agnes AI (free)",
        "base_url": "https://apihub.agnes-ai.com/v1",
        "key_env": "AGNES_API_KEY",
        "headers": {},
    },
    "anthropic": {
        "label": "Anthropic Claude (paid)",
        "base_url": "https://api.anthropic.com/v1",
        "key_env": "ANTHROPIC_API_KEY",
        "headers": {},
    },
    "openai": {
        "label": "OpenAI GPT (paid)",
        "base_url": "https://api.openai.com/v1",
        "key_env": "OPENAI_API_KEY",
        "headers": {},
    },
}


def _provider_key(api):
    spec = API_PROVIDERS.get(api, API_PROVIDERS["nvidia"])
    return os.getenv(spec["key_env"])


def _provider_client(api, key):
    spec = API_PROVIDERS.get(api, API_PROVIDERS["nvidia"])
    headers = {k: v for k, v in spec.get("headers", {}).items() if v}
    if api == "openrouter":
        referer = os.getenv("OPENROUTER_HTTP_REFERER")
        if referer:
            headers["HTTP-Referer"] = referer
    kwargs = {}
    if headers:
        kwargs["default_headers"] = headers
    return OpenAI(base_url=spec["base_url"], api_key=key, timeout=REQUEST_TIMEOUT, **kwargs)


def _load_skills():
    skills_dir = ROOT / "skills"
    skills = {}
    if not skills_dir.is_dir():
        return skills

    def _walk_and_load(path, prefix=""):
        for entry in sorted(path.iterdir()):
            if entry.is_file() and entry.suffix.lower() == ".md" and entry.stem == "SKILL":
                parts = prefix.split("/") if prefix else []
                model_id = "_".join(parts) if parts else entry.stem
                if not model_id.strip():
                    model_id = entry.parent.stem
                content = entry.read_text(encoding="utf-8")
                words = model_id.replace("_", " ").title().split()
                label = " ".join(words) + " AI"
                skills[model_id] = {"label": label, "content": content}
            elif entry.is_file() and entry.suffix.lower() == ".md" and entry.stem != "SKILL":
                if not prefix:
                    model_id = entry.stem
                    words = model_id.replace("-", " ").title().split()
                    label = " ".join(words) + " AI"
                    content = entry.read_text(encoding="utf-8")
                    skills[model_id] = {"label": label, "content": content}
            elif entry.is_dir():
                if not prefix and entry.name == "en":
                    # English skill brain lives here; it is loaded separately
                    # and must not become selectable pseudo-models.
                    continue
                new_prefix = prefix + "/" + entry.name if prefix else entry.name
                _walk_and_load(entry, new_prefix)

    _walk_and_load(skills_dir)
    return skills


def _strip_frontmatter(text: str) -> str:
    """Remove a leading YAML frontmatter block from a SKILL.md file."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            rest = text[end + 4:]
            return rest.lstrip("\n")
    return text


def _load_skill_brain():
    """Load the hidden English skill brain from skills/en/<slug>/SKILL.md.

    Returns {slug: content}. These skills are never exposed as selectable
    models; they are composed into system prompts by the module router.
    """
    brain_dir = ROOT / "skills" / "en"
    brain = {}
    if not brain_dir.is_dir():
        return brain
    for skill_file in sorted(brain_dir.glob("*/SKILL.md")):
        slug = skill_file.parent.name
        try:
            raw = skill_file.read_text(encoding="utf-8")
        except OSError:
            continue
        # Prefer the frontmatter name when present; fall back to folder slug.
        match = re.search(r"^name:\s*([A-Za-z0-9_-]+)\s*$", raw, re.MULTILINE)
        if match:
            slug = match.group(1).strip()
        brain[slug] = _strip_frontmatter(raw).strip()
    return brain


SKILL_BRAIN = _load_skill_brain()
SKILL_ROUTES = CONFIG.get("skill_routes", {}) if isinstance(CONFIG, dict) else {}
PROMPTS = CONFIG.get("prompts", {}) if isinstance(CONFIG, dict) else {}

_BASE_SYSTEM_EN = (
    "You are Meta Ads Expert PRO, a senior paid-media consultant inside the "
    "ForgeHub AI app. Always answer in clear US English. Be direct, practical, "
    "and specific. Never invent metrics, testimonials, results, prices, or "
    "guarantees. If essential data is missing, ask one focused question at a "
    "time before producing the full deliverable. When the user provides enough "
    "data, deliver a complete, structured answer with diagnosis, priorities, "
    "and next steps."
)


def _msg(lang, key, **fmt):
    """Localized backend message: language config -> English config -> key.

    `{placeholder}` values come from **fmt; a missing placeholder never
    breaks the response (the raw template is returned instead).
    """
    lang = normalize_lang(lang)
    text = None
    if lang != "en":
        cfg = get_lang_config(lang=lang)
        text = (cfg.get("messages") or {}).get(key)
    if text is None:
        text = (CONFIG.get("messages") or {}).get(key, key)
    try:
        return text.format(**fmt)
    except Exception:  # noqa: BLE001 - placeholder mismatch must not break
        return text


def _system_prompts(lang="en"):
    """System prompt texts (image/pdf/screenshot/url) for a language."""
    cfg = get_lang_config(lang=lang)
    prompts = cfg.get("system_prompts")
    if isinstance(prompts, dict) and prompts:
        return prompts
    return SYSTEM_PROMPTS


def _skill_brain_for(module_id: str, skill_routes=None, max_chars: int = 42000) -> str:
    """Compose the hidden skill content for a module, primary skill first."""
    routes = SKILL_ROUTES if skill_routes is None else skill_routes
    slugs = routes.get(module_id) or []
    parts = []
    total = 0
    for idx, slug in enumerate(slugs):
        content = SKILL_BRAIN.get(slug)
        if not content:
            continue
        # Primary skill gets the most room; supporting skills are excerpted so
        # a route with several skills stays inside a sane context budget.
        budget = 22000 if idx == 0 else 7000
        excerpt = content[:budget]
        block = f"\n\n--- SKILL: {slug} ---\n{excerpt}"
        if total + len(block) > max_chars:
            remaining = max_chars - total
            if remaining <= 500:
                break
            block = block[:remaining]
        parts.append(block)
        total += len(block)
        if total >= max_chars:
            break
    return "".join(parts).strip()


def _compose_module_system(module_id: str, fallback: str = "", max_chars: int = 42000, lang: str = "en") -> str:
    """Single source of system prompt for a module: base + module brief + skills.

    Base instruction, module brief and skill routes come from the requested
    language's config; the hidden skill brain itself always stays in English.
    """
    cfg = get_lang_config(lang=lang)
    prompts = cfg.get("prompts", {}) or {}
    routes = cfg.get("skill_routes", {}) or {}
    base_system = cfg.get("base_system") or _BASE_SYSTEM_EN
    module_brief = prompts.get(module_id, "") or fallback or ""
    brain = _skill_brain_for(module_id, routes, max_chars=max_chars)
    pieces = [base_system]
    if module_brief:
        pieces.append(f"\n\nMODULE BRIEF:\n{module_brief}")
    if brain:
        pieces.append(f"\n\nHIDDEN EXPERT SKILLS FOR THIS MODULE:\n{brain}")
    return "".join(pieces).strip()


def _build_registry(skills=None):
    if skills is None:
        skills = {}
    default_key = os.getenv("NVIDIA_API_KEY")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    agnes_key = os.getenv("AGNES_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    if not (default_key or openrouter_key or agnes_key or anthropic_key or openai_key):
        raise RuntimeError(
            "No AI key found. Set at least one: "
            "NVIDIA_API_KEY, OPENROUTER_API_KEY, AGNES_API_KEY, ANTHROPIC_API_KEY ou OPENAI_API_KEY. "
            "Local: check your .env. On Vercel: Project Settings -> Environment Variables."
        )
    nvidia_models = {
        "meta/llama-3.1-70b-instruct": {
            "label": "Llama 3.1 70B",
            "provider": "Meta",
            "category": "llm",
            "api_key": os.getenv("NVIDIA_API_KEY_LLAMA", default_key),
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
        },
        "meta/llama-3.1-405b-instruct": {
            "label": "Llama 3.1 405B",
            "provider": "Meta",
            "category": "llm",
            "api_key": os.getenv("NVIDIA_API_KEY_LLAMA405", default_key),
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
        },
        "deepseek-ai/deepseek-r1": {
            "label": "DeepSeek R1",
            "provider": "DeepSeek",
            "category": "llm",
            "api_key": os.getenv("NVIDIA_API_KEY_DEEPSEEK", default_key),
            "params": {"temperature": 0.6, "top_p": 0.95, "max_tokens": 4096},
        },
        "qwen/qwen3.5-397b-a17b": {
            "label": "Qwen 3.5 397B",
            "provider": "Qwen",
            "category": "llm",
            "api_key": os.getenv("NVIDIA_API_KEY_QWEN", default_key),
            "params": {"temperature": 0.6, "top_p": 0.95, "max_tokens": 4096},
        },
        "z-ai/glm-5.2": {
            "label": "GLM-5.2",
            "provider": "Z.ai",
            "category": "llm",
            "api_key": os.getenv("NVIDIA_API_KEY_GLM", default_key),
            "params": {"temperature": 1, "top_p": 1, "max_tokens": 16384},
        },
        "nvidia/nemotron-3-super-120b-instruct": {
            "label": "Nemotron 120B",
            "provider": "NVIDIA",
            "category": "llm",
            "api_key": os.getenv("NVIDIA_API_KEY_NEMOTRON", default_key),
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
        },
        "mistralai/mixtral-8x22b-instruct-v0.1": {
            "label": "Mixtral 8x22B",
            "provider": "Mistral",
            "category": "llm",
            "api_key": os.getenv("NVIDIA_API_KEY_MISTRAL", default_key),
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
        },
        "meta/llama-3.2-90b-vision-instruct": {
            "label": "Llama 3.2 90B Vision",
            "provider": "Meta",
            "category": "vision",
            "api_key": os.getenv("NVIDIA_API_KEY_VISION", default_key),
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048},
        },
    }

    registry = {}
    if default_key:
        registry.update(nvidia_models)

    if openrouter_key:
        registry["openrouter/llama-3.3-70b-free"] = {
            "label": "Llama 3.3 70B (OpenRouter Free)",
            "provider": "OpenRouter",
            "category": "llm",
            "api": "openrouter",
            "api_key": openrouter_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
            "underlying": APP_MODELS.get("openrouter_text") or os.getenv(
                "OPENROUTER_TEXT_MODEL", "meta-llama/llama-3.3-70b-instruct:free"
            ),
        }
        registry["openrouter/gemma-4-31b-vision-free"] = {
            "label": "Gemma 4 31B Vision (OpenRouter Free)",
            "provider": "OpenRouter",
            "category": "vision",
            "api": "openrouter",
            "api_key": openrouter_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048},
            "underlying": APP_MODELS.get("openrouter_vision") or os.getenv(
                "OPENROUTER_VISION_MODEL", "google/gemma-4-31b-it:free"
            ),
        }

    if agnes_key:
        registry["agnes/agnes-2.0-flash"] = {
            "label": "Agnes 2.0 Flash (Agnes AI Free)",
            "provider": "Agnes AI",
            "category": "llm",
            "api": "agnes",
            "api_key": agnes_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
            "underlying": APP_MODELS.get("agnes_text") or os.getenv(
                "AGNES_TEXT_MODEL", "agnes-2.0-flash"
            ),
            # Agnes free tier returns 503 on ~1/3 of calls; retry recovers (NOTAS-API).
            "retry": True,
        }

    if anthropic_key:
        claude_model = APP_MODELS.get("anthropic_text") or os.getenv(
            "ANTHROPIC_TEXT_MODEL", "claude-sonnet-4-5"
        )
        registry["anthropic/claude-sonnet"] = {
            "label": "Claude Sonnet (Anthropic)",
            "provider": "Anthropic",
            "category": "llm",
            "api": "anthropic",
            "api_key": anthropic_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
            "underlying": claude_model,
        }
        registry["anthropic/claude-vision"] = {
            "label": "Claude Vision (Anthropic)",
            "provider": "Anthropic",
            "category": "vision",
            "api": "anthropic",
            "api_key": anthropic_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048},
            "underlying": claude_model,
        }

    if openai_key:
        registry["openai/gpt-4o-mini"] = {
            "label": "GPT-4o Mini (OpenAI)",
            "provider": "OpenAI",
            "category": "llm",
            "api": "openai",
            "api_key": openai_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
            "underlying": APP_MODELS.get("openai_text") or os.getenv(
                "OPENAI_TEXT_MODEL", "gpt-4o-mini"
            ),
        }
        registry["openai/gpt-4o"] = {
            "label": "GPT-4o Vision (OpenAI)",
            "provider": "OpenAI",
            "category": "vision",
            "api": "openai",
            "api_key": openai_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048},
            "underlying": APP_MODELS.get("openai_vision") or os.getenv(
                "OPENAI_VISION_MODEL", "gpt-4o"
            ),
        }

    # Expert skills run on the configured expert model when available,
    # otherwise fall back to OpenRouter, then Agnes.
    expert_cfg = APP_MODELS.get("expert_underlying", DEFAULT_MODEL)
    if expert_cfg in registry:
        expert_entry = registry[expert_cfg]
    elif "openrouter/llama-3.3-70b-free" in registry:
        expert_entry = registry["openrouter/llama-3.3-70b-free"]
    elif "agnes/agnes-2.0-flash" in registry:
        expert_entry = registry["agnes/agnes-2.0-flash"]
    else:
        expert_entry = next(
            (e for e in registry.values() if e.get("category") == "llm"), {}
        )

    for skill_id, skill in skills.items():
        registry[skill_id] = {
            "label": skill["label"],
            "provider": "Expert",
            "category": "llm",
            "api": expert_entry.get("api", "nvidia"),
            "api_key": expert_entry.get("api_key"),
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
            "underlying": expert_entry.get("underlying", expert_cfg),
            "skill_content": skill["content"],
        }

    for entry in registry.values():
        entry.setdefault("api", "nvidia")

    return registry


def _strip_vercel_prefix(asgi_app):
    """ASGI wrapper: normalize paths mangled by Vercel's catch-all rewrite.

    Behind `vercel.json`'s `/(.*) -> /api/index` rewrite, the function can
    receive the rewritten path ("/api/index" or "/api/index/<real path>")
    instead of the path the visitor asked for, so no FastAPI route matches
    and even "/" answers 404 {"detail":"Not Found"}. Strip that prefix
    before dispatching. Lives here (not in api/index.py) so EVERY entry
    point (api/index.py, server.py) gets it, whichever one Vercel serves.
    Normal paths pass through untouched, so local runs are unaffected.
    """
    prefixes = ("/api/index.py", "/api/index")

    async def wrapped(scope, receive, send):
        if scope.get("type") in ("http", "websocket"):
            # TEMPORARY PROBE: /...?__probe=1 echoes the raw ASGI routing info
            # (path/root_path/headers) so we can see exactly what Vercel hands
            # the function behind the rewrite. Remove after diagnosis.
            if scope["type"] == "http" and b"__probe=1" in (
                scope.get("query_string") or b""
            ):
                payload = json.dumps(
                    {
                        "path": scope.get("path"),
                        "raw_path": (scope.get("raw_path") or b"").decode(
                            "utf-8", "replace"
                        ),
                        "root_path": scope.get("root_path"),
                        "method": scope.get("method"),
                        "query_string": (scope.get("query_string") or b"").decode(
                            "utf-8", "replace"
                        ),
                        "headers": [
                            [k.decode("latin-1"), v.decode("latin-1")]
                            for k, v in (scope.get("headers") or [])
                        ],
                    }
                ).encode()
                await send(
                    {
                        "type": "http.response.start",
                        "status": 200,
                        "headers": [
                            [b"content-type", b"application/json"],
                            [b"content-length", str(len(payload)).encode()],
                        ],
                    }
                )
                await send({"type": "http.response.body", "body": payload})
                return
            path = scope.get("path") or ""
            for prefix in prefixes:
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
        await asgi_app(scope, receive, send)

    return wrapped


def create_app():
    skills = _load_skills()
    model_registry = _build_registry(skills)
    default_key = os.getenv("NVIDIA_API_KEY")
    clients = {}

    default_model_id = (
        DEFAULT_MODEL
        if DEFAULT_MODEL in model_registry
        else next(
            (m for m, e in model_registry.items() if e.get("category") == "llm"),
            DEFAULT_MODEL,
        )
    )

    def client_for(model_id):
        entry = model_registry.get(model_id)
        api = entry.get("api", "nvidia") if entry else "nvidia"
        key = entry["api_key"] if entry else _provider_key(api)
        params = entry["params"] if entry else {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096}
        cache_key = (api, key)
        if cache_key not in clients:
            clients[cache_key] = _provider_client(api, key)
        return clients[cache_key], params

    def _vision_target():
        """Pick the vision route: NVIDIA -> GPT-4o -> Claude -> OpenRouter free."""
        candidates = [
            APP_MODELS.get("vision", "meta/llama-3.2-90b-vision-instruct"),
            "openai/gpt-4o",
            "anthropic/claude-vision",
            "openrouter/gemma-4-31b-vision-free",
        ]
        for vision_id in candidates:
            if vision_id in model_registry:
                client, _params = client_for(vision_id)
                return client, model_registry[vision_id].get("underlying", vision_id)
        return None, None

    def _create_completion(client, model, messages, params, retry=False):
        # Agnes free tier: ~1/3 of calls fail with 503; backoff retry recovers.
        attempts = 3 if retry else 1
        last_exc = None
        for attempt in range(attempts):
            try:
                return client.chat.completions.create(
                    model=model, messages=messages, stream=True, **params,
                )
            except Exception as exc:  # noqa: BLE001 - re-raised after retries
                last_exc = exc
                if attempt < attempts - 1:
                    time.sleep(2 ** attempt)
        raise last_exc

    def _sse_stream(client, model, messages, params, retry=False):
        start = time.monotonic()
        first_token_at = None
        try:
            completion = _create_completion(client, model, messages, params, retry)
            for chunk in completion:
                if not getattr(chunk, "choices", None):
                    continue
                choice = chunk.choices[0]
                delta = getattr(choice, "delta", None)
                if delta is None:
                    continue
                content = getattr(delta, "content", None)
                if content:
                    if first_token_at is None:
                        first_token_at = time.monotonic()
                        ttft_ms = int((first_token_at - start) * 1000)
                        yield f"event: meta\ndata: {json.dumps({'ttft_ms': ttft_ms})}\n\n"
                    yield f"data: {json.dumps({'content': content})}\n\n"
            total_ms = int((time.monotonic() - start) * 1000)
            yield f"event: done\ndata: {json.dumps({'total_ms': total_ms})}\n\n"
        except Exception as exc:
            yield f"event: error\ndata: {json.dumps({'message': str(exc)})}\n\n"

    def _sse_response(stream_gen):
        return StreamingResponse(
            stream_gen,
            media_type="text/event-stream",
            headers={
                "X-Accel-Buffering": "no",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )

    def _stream_analysis(user_prompt: str, model_id: str = None, module_id: str = None, lang: str = "en"):
        lang = normalize_lang(lang)
        if module_id:
            model_id = default_model_id
            entry = model_registry.get(model_id)
            if not entry:
                return JSONResponse({"error": _msg(lang, "model_not_found")}, status_code=500)
            system_content = _compose_module_system(module_id, lang=lang)
        else:
            if model_id is None:
                model_id = CONFIG.get("app_id", "pro")
            entry = model_registry.get(model_id)
            if not entry:
                return JSONResponse({"error": _msg(lang, "model_not_found")}, status_code=500)
            system_content = entry.get("skill_content", "")

        underlying = entry.get("underlying", model_id)
        client, params = client_for(model_id)

        messages = []
        if system_content:
            messages.append({"role": "system", "content": system_content})
        messages.append({"role": "user", "content": user_prompt})

        return _sse_response(_sse_stream(client, underlying, messages, params, retry=bool(entry.get("retry"))))

    def _detect_platform(url: str) -> str:
        for pattern, name in PLATFORM_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE):
                return name
        return ""

    def _detect_product_type(text: str) -> list:
        found = []
        text_lower = text.lower()
        for ptype, keywords in PRODUCT_TYPE_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    found.append(ptype)
                    break
        return found

    def _fetch_and_clean_url(url: str, lang: str = "en") -> dict:
        lang = normalize_lang(lang)
        if _requests is None:
            raise HTTPException(500, _msg(lang, "requests_not_installed"))
        if BeautifulSoup is None:
            raise HTTPException(500, _msg(lang, "bs4_not_installed"))

        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname or ""

        if parsed.scheme == "file":
            raise HTTPException(400, _msg(lang, "file_url_not_allowed"))
        if hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            raise HTTPException(400, _msg(lang, "local_url_not_allowed"))
        if hostname.endswith(".local") or hostname.endswith(".internal"):
            raise HTTPException(400, _msg(lang, "internal_url_not_allowed"))

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        try:
            resp = _requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            resp.raise_for_status()
        except _requests.Timeout:
            raise HTTPException(408, _msg(lang, "page_timeout"))
        except _requests.HTTPError as e:
            code = e.response.status_code
            raise HTTPException(code, _msg(lang, "http_error", code=code))
        except _requests.ConnectionError:
            raise HTTPException(502, _msg(lang, "cannot_connect"))
        except _requests.RequestException as e:
            raise HTTPException(400, _msg(lang, "url_error", detail=str(e)[:120]))

        ct = resp.headers.get("content-type", "")
        if "text/html" not in ct and "application/xhtml" not in ct:
            raise HTTPException(400, _msg(lang, "not_html"))

        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else ""
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag["content"].strip()

        for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "noscript", "iframe", "form", "svg", "link", "meta", "noscript"]):
            tag.decompose()

        body = soup.find("body")
        text = body.get_text(separator="\n", strip=True) if body else ""
        text = re.sub(r"\n{4,}", "\n\n", text)
        text = text[:10000]

        return {"title": title, "description": meta_desc, "content": text}

    app = FastAPI()
    static_dir = ROOT / "static"

    @app.get("/")
    def index():
        return FileResponse(static_dir / "index.html")

    @app.get("/api/models")
    def list_models():
        return JSONResponse([
            {
                "id": model_id,
                "label": entry["label"],
                "provider": entry["provider"],
                "category": entry.get("category", "llm"),
            }
            for model_id, entry in model_registry.items()
        ])

    @app.get("/api/health")
    def health():
        return JSONResponse({
            "status": "ok",
            "providers": [a for a in API_PROVIDERS if _provider_key(a)],
            "models": list(model_registry.keys()),
        })

    @app.get("/api/branding")
    def branding(app_id: str = None, lang: str = "en"):
        lang = normalize_lang(lang)
        if app_id:
            try:
                cfg = get_lang_config(app_id, lang)
                reload_config()
                return JSONResponse(cfg)
            except FileNotFoundError:
                raise HTTPException(404, _msg(lang, "app_not_found", app_id=app_id))
        return JSONResponse(get_lang_config(None, lang))

    @app.get("/api/configs")
    def available_configs():
        return JSONResponse(list_configs())

    @app.post("/api/chat")
    async def chat(request: Request):
        body = await request.json()
        messages = body.get("messages", [])
        model = (body.get("model") or default_model_id).strip()
        module_id = (body.get("module") or body.get("module_id") or "").strip()
        lang = normalize_lang(body.get("lang"))

        entry = model_registry.get(model, {})
        if module_id:
            # Module routing is the single source of the system prompt: the
            # hidden EN skills for that module. Drop any system messages the
            # client sent so the brain is not duplicated or overridden.
            if entry.get("skill_content") or model not in model_registry:
                model = default_model_id
                entry = model_registry.get(model, {})
            system_content = _compose_module_system(module_id, lang=lang)
            if system_content:
                messages = [{"role": "system", "content": system_content}] + [
                    m for m in messages if m.get("role") != "system"
                ]
        else:
            skill_content = entry.get("skill_content")
            if skill_content:
                messages = [{"role": "system", "content": skill_content}] + messages

        client, params = client_for(model)
        api_model = entry.get("underlying", model)

        return _sse_response(_sse_stream(client, api_model, messages, params, retry=bool(entry.get("retry"))))

    @app.post("/api/upload-image")
    async def upload_image(file: UploadFile = File(...), lang: str = "en"):
        lang = normalize_lang(lang)
        if not UPLOADS.get("image", True):
            raise HTTPException(400, _msg(lang, "image_disabled"))

        valid_ext = {"jpg", "jpeg", "png", "webp"}
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in valid_ext:
            raise HTTPException(400, _msg(lang, "image_invalid_format"))

        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(400, _msg(lang, "image_too_large"))

        b64 = base64.b64encode(contents).decode("utf-8")
        mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
        mime = mime_map.get(ext, "image/jpeg")

        system_prompt = _compose_module_system(
            "upload-image",
            fallback=_system_prompts(lang).get("image", "Analyze this image."),
            max_chars=24000,
            lang=lang,
        )
        vision_client, vision_model = _vision_target()
        if vision_client is None:
            raise HTTPException(503, _msg(lang, "vision_not_configured"))

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text", "text": _msg(lang, "analyze_image_prompt")},
            ]},
        ]

        vision_params = {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048}
        return _sse_response(_sse_stream(vision_client, vision_model, messages, vision_params))

    @app.post("/api/upload-pdf")
    async def upload_pdf(file: UploadFile = File(...), lang: str = "en"):
        lang = normalize_lang(lang)
        if not UPLOADS.get("pdf", True):
            raise HTTPException(400, _msg(lang, "pdf_disabled"))

        if PdfReader is None:
            raise HTTPException(500, _msg(lang, "pypdf_not_installed"))

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(400, _msg(lang, "pdf_invalid_format"))
        contents = await file.read()
        if len(contents) > 20 * 1024 * 1024:
            raise HTTPException(400, _msg(lang, "pdf_too_large"))

        safe_name = re.sub(r"[^\w\.\-]", "_", file.filename)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        try:
            tmp.write(contents)
            tmp.close()
            reader = PdfReader(tmp.name)
            text_parts = [p.extract_text() or "" for p in reader.pages]
            full_text = "\n".join(text_parts).strip()
            if len(full_text) < 50:
                return JSONResponse({"error": _msg(lang, "pdf_no_text")}, status_code=400)
            if len(full_text) > 15000:
                full_text = full_text[:15000] + "\n" + _msg(lang, "pdf_truncated")
        finally:
            os.unlink(tmp.name)

        instruction = _system_prompts(lang).get("pdf", "Analyze the document.")

        return _stream_analysis(
            f"{instruction}\n\n{_msg(lang, 'pdf_content_label')} ({safe_name}):\n\n{full_text}",
            module_id="upload-pdf",
            lang=lang,
        )

    @app.post("/api/upload-screenshot")
    async def upload_screenshot(file: UploadFile = File(...), lang: str = "en"):
        lang = normalize_lang(lang)
        if not UPLOADS.get("screenshot", True):
            raise HTTPException(400, _msg(lang, "screenshot_disabled"))

        valid_ext = {"jpg", "jpeg", "png", "webp"}
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in valid_ext:
            raise HTTPException(400, _msg(lang, "image_invalid_format"))
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(400, _msg(lang, "screenshot_too_large"))

        b64 = base64.b64encode(contents).decode("utf-8")
        mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
        mime = mime_map.get(ext, "image/jpeg")

        system_prompt = _compose_module_system(
            "upload-screenshot",
            fallback=_system_prompts(lang).get("screenshot", ""),
            max_chars=24000,
            lang=lang,
        )
        if not system_prompt:
            raise HTTPException(400, _msg(lang, "screenshot_unavailable"))

        vision_client, vision_model = _vision_target()
        if vision_client is None:
            raise HTTPException(503, _msg(lang, "vision_not_configured"))

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text", "text": _msg(lang, "analyze_screenshot_prompt")},
            ]},
        ]

        vision_params = {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048}
        return _sse_response(_sse_stream(vision_client, vision_model, messages, vision_params))

    @app.post("/api/analyze-url")
    async def analyze_url(request: Request):
        body = await request.json()
        lang = normalize_lang(body.get("lang"))
        if not UPLOADS.get("url", True):
            raise HTTPException(400, _msg(lang, "url_disabled"))

        url = body.get("url", "").strip()
        analysis_type = body.get("type", "lp")

        if not url:
            raise HTTPException(400, _msg(lang, "no_url"))
        if not url.startswith("http://") and not url.startswith("https://"):
            raise HTTPException(400, _msg(lang, "url_must_start"))

        page_data = _fetch_and_clean_url(url, lang)

        platform = _detect_platform(url)
        product_types = _detect_product_type(url + " " + page_data["title"] + " " + page_data["content"][:3000])
        platform_info = f"{_msg(lang, 'detected_platform', value=platform)}\n" if platform else ""
        product_info = f"{_msg(lang, 'detected_product_type', value=', '.join(product_types))}\n" if product_types else ""

        url_prompts = _system_prompts(lang).get("url", {})
        instruction = url_prompts.get(analysis_type) or url_prompts.get("lp", "Analyze this page.")
        user_content = (
            f"{instruction}\n\n"
            f"{_msg(lang, 'analyzed_url', url=url)}\n"
            f"{platform_info}"
            f"{product_info}"
            f"{_msg(lang, 'page_title', value=page_data['title'])}\n"
            f"{_msg(lang, 'meta_description', value=page_data['description'])}\n\n"
            f"{_msg(lang, 'extracted_content')}\n{page_data['content']}"
        )
        route_by_type = {"lp": "url-lp", "loja": "url-loja", "app": "url-app"}
        return _stream_analysis(
            user_content,
            module_id=route_by_type.get(analysis_type, "url-lp"),
            lang=lang,
        )

    @app.post("/api/embeddings")
    async def embeddings(request: Request):
        body = await request.json()
        text = body.get("input", body.get("text", ""))
        model = body.get("model", "nvidia/nv-embedqa-e5-v5")
        if not default_key:
            return JSONResponse({"error": _msg(body.get("lang"), "embeddings_need_key")}, status_code=503)
        client_obj = OpenAI(base_url=BASE_URL, api_key=default_key, timeout=REQUEST_TIMEOUT)
        try:
            start = time.monotonic()
            result = client_obj.embeddings.create(
                model=model,
                input=[text] if isinstance(text, str) else text,
                extra_body={"input_type": "query"},
            )
            total_ms = int((time.monotonic() - start) * 1000)
            return JSONResponse({
                "model": model,
                "dimension": len(result.data[0].embedding),
                "total_ms": total_ms,
                "embedding_preview": result.data[0].embedding[:8],
            })
        except Exception as exc:
            return JSONResponse({"error": str(exc)}, status_code=500)

    return _strip_vercel_prefix(app)
