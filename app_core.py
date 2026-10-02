import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import tempfile
import time
import urllib.parse
import uuid
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


_SECRET_ENV_KEYS = (
    "OPENROUTER_API_KEY",
    "AGNES_API_KEY",
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
)

_SECRET_PATTERNS = (
    re.compile(r"sk-or-v1-[A-Za-z0-9\-_]{8,}"),
    re.compile(r"sk-[A-Za-z0-9\-_]{8,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9\-_\.]{8,}"),
)


def _scrub_secrets(text: str) -> str:
    """Redact API keys/secrets from text before it goes to the client.

    Provider errors can echo the offending value back (e.g. an invalid
    model-id error quoting the string that was sent). Never let a secret
    reach the browser inside an error message.
    """
    out = text or ""
    for env_key in _SECRET_ENV_KEYS:
        value = os.environ.get(env_key)
        if value and len(value) >= 8:
            out = out.replace(value, "***")
    for pattern in _SECRET_PATTERNS:
        out = pattern.sub("***", out)
    return out


def _safe_model_id(value, fallback: str) -> str:
    """Return `value` if it looks like a provider model ID (``vendor/model``).

    Guards against a secret or other garbage landing in a *_MODEL setting:
    a value that looks like an API key must never be sent as the model ID.
    """
    v = (value or "").strip()
    if not v or v.startswith("sk-") or "/" not in v:
        return fallback
    return v


# ---------------------------------------------------------------------------
# Free-model fallback chains (OpenRouter). Free models draw from a SHARED
# upstream pool per model: when that pool is saturated the provider answers
# 429 ("temporarily rate-limited upstream") even though the API key is fine.
# Rolling the request over to the next free model turns that hard failure
# into an invisible retry. Chains verified against the public OpenRouter
# catalog on 2026-10-01 (all :free, big-context, text-capable; the vision
# chain is image-capable). Override with OPENROUTER_TEXT_FALLBACK_MODELS /
# OPENROUTER_VISION_FALLBACK_MODELS (comma-separated model IDs).
# ---------------------------------------------------------------------------
_OPENROUTER_TEXT_FALLBACKS = (
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "qwen/qwen3.8-27b:free",
)
_OPENROUTER_VISION_FALLBACKS = (
    "google/gemma-4-26b-a4b-it:free",
    "qwen/qwen3.8-27b:free",
)


def _fallback_chain(env_key: str, defaults, primary: str) -> list:
    """Ordered fallback model IDs after `primary` (deduped, junk filtered)."""
    raw = os.getenv(env_key, "")
    ids = [p.strip() for p in raw.split(",")] if raw.strip() else list(defaults)
    chain = []
    for mid in ids:
        mid = _safe_model_id(mid, "")
        if mid and mid != primary and mid not in chain:
            chain.append(mid)
    return chain


def _friendly_ai_error(exc: Exception, lang: str = "en") -> str:
    """Short, localized, user-facing text for a provider failure.

    Raw provider payloads (429 JSON blobs, SDK reprs) are technical noise
    for end users — and can echo request details — so the client only ever
    sees a calm "busy, try again" style message in its own language.
    """
    raw = str(exc) or ""
    low = raw.lower()
    if "429" in raw or "rate" in low or "temporarily" in low or "busy" in low:
        return _msg(lang, "ai_busy")
    if "401" in raw or "403" in raw or "auth" in low or "api key" in low:
        return _msg(lang, "ai_auth_error")
    if "timeout" in low or "timed out" in low:
        return _msg(lang, "ai_timeout")
    return _msg(lang, "ai_generic_error")


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
    "Meta Ads Expert PRO app. Always answer in clear US English. Be direct, practical, "
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
        text_underlying = _safe_model_id(
            APP_MODELS.get("openrouter_text") or os.getenv("OPENROUTER_TEXT_MODEL"),
            "qwen/qwen3.8-27b:free",
        )
        registry["openrouter/llama-3.3-70b-free"] = {
            "label": "Llama 3.3 70B (OpenRouter Free)",
            "provider": "OpenRouter",
            "category": "llm",
            "api": "openrouter",
            "api_key": openrouter_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
            "underlying": text_underlying,
            # When the primary free model answers 429 (shared pool busy),
            # the request rolls over to these instead of failing.
            "fallback_models": _fallback_chain(
                "OPENROUTER_TEXT_FALLBACK_MODELS",
                _OPENROUTER_TEXT_FALLBACKS,
                text_underlying,
            ),
        }
        vision_underlying = _safe_model_id(
            APP_MODELS.get("openrouter_vision") or os.getenv("OPENROUTER_VISION_MODEL"),
            "google/gemma-4-31b-it:free",
        )
        registry["openrouter/gemma-4-31b-vision-free"] = {
            "label": "Gemma 4 31B Vision (OpenRouter Free)",
            "provider": "OpenRouter",
            "category": "vision",
            "api": "openrouter",
            "api_key": openrouter_key,
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048},
            "underlying": vision_underlying,
            "fallback_models": _fallback_chain(
                "OPENROUTER_VISION_FALLBACK_MODELS",
                _OPENROUTER_VISION_FALLBACKS,
                vision_underlying,
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


# ---------------------------------------------------------------------------
# Tracking (Meta Pixel + Conversions API) — storage, webhook sales, CAPI.
#
# Config and sales are kept server-side, keyed by an unguessable per-user
# key that also sits in the webhook URL the user pastes into their checkout.
# Locally this is a JSON file under data/; on serverless (VERCEL) it falls
# back to /tmp, which is ephemeral — durable storage needs a KV/DB (phase 2).
# The CAPI token lives ONLY server-side: it is never returned to the
# browser, never put in a URL we generate, and never logged (all error
# paths scrub secrets via _scrub_secrets).
# ---------------------------------------------------------------------------
_GRAPH_BASE = os.getenv("META_GRAPH_BASE", "https://graph.facebook.com/v21.0")
_TRK_KEY_RE = re.compile(r"^[a-f0-9]{32,64}$")
_TRK_PIXEL_RE = re.compile(r"^\d{8,20}$")
_TRK_EVENTS = ["PageView", "ViewContent", "AddToCart", "InitiateCheckout",
               "AddPaymentInfo", "Purchase", "Lead"]


def _trk_data_dir() -> Path:
    env = os.getenv("META_ADS_DATA_DIR")
    if env:
        p = Path(env)
    elif os.getenv("VERCEL"):
        p = Path("/tmp/meta-ads-data")
    else:
        p = ROOT / "data"
    try:
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception:
        p = Path(tempfile.gettempdir()) / "meta-ads-data"
        p.mkdir(parents=True, exist_ok=True)
        return p


def _trk_load() -> dict:
    try:
        return json.loads((_trk_data_dir() / "tracking_store.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def _trk_save_all(data: dict) -> None:
    path = _trk_data_dir() / "tracking_store.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def _sb_target():
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_KEY", "")
    return (url, key) if url and key else (None, None)


def _sb_req(method, table, params=None, payload=None):
    url, key = _sb_target()
    if not url or _requests is None:
        raise RuntimeError("supabase_unavailable")
    headers = {"apikey": key, "Authorization": f"Bearer {key}",
               "Content-Type": "application/json",
               "Prefer": "resolution=merge-duplicates,return=minimal"}
    resp = _requests.request(method, f"{url}/rest/v1/{table}", params=params,
                             json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    if resp.status_code == 204 or not resp.content:
        return None
    return resp.json()


def _store_get(key):
    """Return {'config': {...}, 'sales': [...], 'last_test_ok': ...} or None.
    Supabase when SUPABASE_URL + SUPABASE_SERVICE_KEY are set, else local file."""
    url, _ = _sb_target()
    if not url:
        return _trk_load().get(key)
    try:
        sale_rows = _sb_req("GET", "trk_sales",
                            params={"key": f"eq.{key}", "select": "record",
                                    "order": "ts.desc", "limit": "500"}) or []
        sales = [r["record"] for r in reversed(sale_rows)
                 if isinstance(r.get("record"), dict)]
        rows = _sb_req("GET", "trk_configs", params={"key": f"eq.{key}", "select": "*"})
        if not rows:
            # Webhook-open keys have sales but no config row yet.
            return {"config": {}, "sales": sales, "last_test_ok": None} if sales else None
        row = rows[0]
        cfg = {"pixel_id": row.get("pixel_id") or "",
               "domain": row.get("domain") or "",
               "test_code": row.get("test_code") or "",
               "events": row.get("events") or []}
        if row.get("token"):
            cfg["token"] = row["token"]
        return {"config": cfg, "sales": sales,
                "last_test_ok": row.get("last_test_ok")}
    except Exception as exc:
        print(f"[tracking] storage read error: {_scrub_secrets(str(exc))[:200]}",
              file=sys.stderr)
        return None


def _store_put_config(key, cfg, last_test_ok):
    url, _ = _sb_target()
    if not url:
        store = _trk_load()
        rec = store.get(key) or {"config": {}, "sales": []}
        rec["config"] = cfg
        if last_test_ok is not None:
            rec["last_test_ok"] = last_test_ok
        store[key] = rec
        _trk_save_all(store)
        return
    row = {"key": key,
           "pixel_id": cfg.get("pixel_id", ""),
           "token": cfg.get("token") or None,
           "test_code": cfg.get("test_code", ""),
           "domain": cfg.get("domain", ""),
           "events": cfg.get("events") or [],
           "last_test_ok": last_test_ok}
    _sb_req("POST", "trk_configs", payload=row)


def _store_add_sale(key, record):
    url, _ = _sb_target()
    if not url:
        store = _trk_load()
        rec = store.get(key) or {"config": {}, "sales": []}
        rec.setdefault("sales", []).append(record)
        rec["sales"] = rec["sales"][-500:]
        store[key] = rec
        _trk_save_all(store)
        return
    _sb_req("POST", "trk_sales",
            payload={"event_id": record["id"], "key": key, "ts": record["ts"],
                     "method": record["method"], "record": record})


def _trk_clean(value, maxlen=200):
    if value is None:
        return ""
    s = "".join(ch for ch in str(value) if ch.isprintable() or ch == " ")
    return s.strip()[:maxlen]


def _trk_amount(value):
    try:
        f = float(str(value).replace(" ", "").replace(",", "."))
    except Exception:
        return None
    if f != f or f in (float("inf"), float("-inf")) or f < 0 or f > 100_000_000:
        return None
    return round(f, 2)


def _trk_hash(value, kind):
    """SHA-256 of normalized PII, per Meta's Conversions API requirements."""
    if not value:
        return None
    v = str(value).strip().lower()
    if kind == "ph":
        v = re.sub(r"\D", "", v)
    if kind == "fn":
        v = v.split(" ")[0]
    if not v:
        return None
    return hashlib.sha256(v.encode("utf-8")).hexdigest()


def _trk_method(raw):
    s = _trk_clean(raw, 60).lower()
    if "pix" in s:
        return "pix"
    if "billet" in s or "boleto" in s:
        return "boleto"
    if "card" in s or "credit" in s or "cart" in s or "credito" in s or "crédito" in s:
        return "card"
    return "other"


def _trk_status(raw):
    s = _trk_clean(raw, 80).lower()
    if any(t in s for t in ("refund", "chargeback", "cancel", "estorn")):
        return "refunded"
    if any(t in s for t in ("paid", "approved", "complete", "succeeded", "pago", "aprovad", "confirmed")):
        return "paid"
    return "pending"


def _trk_utms(*dicts):
    out = {}
    for d in dicts:
        if not isinstance(d, dict):
            continue
        for k in ("utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbp", "fbc"):
            if not out.get(k) and d.get(k):
                out[k] = _trk_clean(d.get(k), 200)
    return out


def _trk_extract_sale(body):
    """Best-effort normalization of checkout webhooks (Hotmart, Kiwify,
    Stripe, generic). Returns only non-PII fields plus the raw PII values
    under _pii (used once for the CAPI send, never persisted)."""
    if not isinstance(body, dict):
        return None
    data = body.get("data") if isinstance(body.get("data"), dict) else {}
    purchase = data.get("purchase") if isinstance(data.get("purchase"), dict) else {}
    buyer = data.get("buyer") if isinstance(data.get("buyer"), dict) else {}
    price = purchase.get("price") if isinstance(purchase.get("price"), dict) else {}
    payment = purchase.get("payment") if isinstance(purchase.get("payment"), dict) else {}
    obj = data.get("object") if isinstance(data.get("object"), dict) else {}
    cust = obj.get("customer_details") if isinstance(obj.get("customer_details"), dict) else {}
    utms = _trk_utms(body, data, purchase, obj,
                     body.get("metadata") if isinstance(body.get("metadata"), dict) else {},
                     obj.get("metadata") if isinstance(obj.get("metadata"), dict) else {})
    base = {"utm_source": utms.get("utm_source", ""), "utm_medium": utms.get("utm_medium", ""),
            "utm_campaign": utms.get("utm_campaign", ""), "utm_term": utms.get("utm_term", ""),
            "utm_content": utms.get("utm_content", ""),
            "_pii": {"fbp": utms.get("fbp"), "fbc": utms.get("fbc")}}
    if purchase:  # Hotmart v2
        base.update(platform="hotmart", amount=_trk_amount(price.get("value")),
                    currency=_trk_clean(price.get("currency_code"), 3).upper() or "BRL",
                    method=_trk_method(payment.get("type")),
                    status=_trk_status(purchase.get("status") or body.get("event")))
        base["_pii"].update(email=buyer.get("email"), name=buyer.get("name"),
                            phone=buyer.get("checkout_phone") or buyer.get("phone"))
        return base
    if obj and (body.get("type") or "").startswith("checkout.session"):  # Stripe
        cents = obj.get("amount_total")
        base.update(platform="stripe",
                    amount=(round(cents / 100, 2) if isinstance(cents, (int, float)) else _trk_amount(cents)),
                    currency=_trk_clean(obj.get("currency"), 3).upper() or "USD",
                    method=_trk_method(" ".join(obj.get("payment_method_types") or [])),
                    status="paid" if obj.get("payment_status") == "paid" else "pending")
        base["_pii"].update(email=cust.get("email"), name=cust.get("name"), phone=cust.get("phone"))
        return base
    if body.get("order_status") or body.get("payment_method"):  # Kiwify-like
        base.update(platform="kiwify",
                    amount=_trk_amount(body.get("order_amount") or body.get("amount") or body.get("value")),
                    currency=_trk_clean(body.get("currency"), 3).upper() or "BRL",
                    method=_trk_method(body.get("payment_method")),
                    status=_trk_status(body.get("order_status") or body.get("status")))
        base["_pii"].update(email=body.get("email"), name=body.get("name"), phone=body.get("phone"))
        return base
    # Generic flat payload
    base.update(platform="generic",
                amount=_trk_amount(body.get("amount") or body.get("value") or body.get("price")),
                currency=_trk_clean(body.get("currency"), 3).upper() or "BRL",
                method=_trk_method(body.get("method") or body.get("payment_method")),
                status=_trk_status(body.get("status") or body.get("event")))
    base["_pii"].update(email=body.get("email"), name=body.get("name"), phone=body.get("phone"))
    return base


def _trk_sale_event(status, method):
    if status == "paid":
        return "Purchase"
    if status == "pending":
        return "AddPaymentInfo" if method == "boleto" else "InitiateCheckout"
    return None


def _capi_send(cfg, event_name, event_id, value=None, currency=None, pii=None, test_code=None, utms=None):
    """Send one event to the Conversions API. Returns (ok, short_detail).

    The token travels in the POST body only; failures return short codes,
    never provider payloads, and stderr logging is secret-scrubbed."""
    pixel = cfg.get("pixel_id")
    token = cfg.get("token")
    if not pixel or not token:
        return False, "not_configured"
    if _requests is None:
        return False, "no_http_client"
    pii = pii or {}
    user_data = {}
    for field, kind in (("email", "em"), ("phone", "ph"), ("name", "fn")):
        h = _trk_hash(pii.get(field), kind)
        if h:
            user_data[kind] = [h]
    if pii.get("fbp"):
        user_data["fbp"] = pii["fbp"]
    if pii.get("fbc"):
        user_data["fbc"] = pii["fbc"]
    event = {"event_name": event_name, "event_time": int(time.time()),
             "event_id": event_id, "action_source": "system_generated",
             "user_data": user_data}
    custom = {}
    if value is not None:
        custom["value"] = value
    if currency:
        custom["currency"] = currency
    for k, v in (utms or {}).items():
        if v:
            custom[k] = v
    if custom:
        event["custom_data"] = custom
    payload = {"data": [event], "access_token": token}
    if test_code:
        payload["test_event_code"] = test_code
    try:
        r = _requests.post(f"{_GRAPH_BASE}/{pixel}/events", json=payload, timeout=15)
        if r.status_code == 200:
            return True, "sent"
        return False, f"meta_{r.status_code}"
    except Exception as exc:
        print(f"[tracking] capi send error: {_scrub_secrets(str(exc))[:200]}", file=sys.stderr)
        return False, "network_error"


def _capi_test(cfg):
    """Validate pixel + token against the Graph API. Returns (ok, detail)."""
    pixel = cfg.get("pixel_id")
    token = cfg.get("token")
    if not pixel or not token:
        return False, "not_configured"
    if _requests is None:
        return False, "no_http_client"
    try:
        r = _requests.get(f"{_GRAPH_BASE}/{pixel}",
                          params={"fields": "id,name", "access_token": token}, timeout=15)
        return (r.status_code == 200), ("ok" if r.status_code == 200 else f"meta_{r.status_code}")
    except Exception as exc:
        print(f"[tracking] capi test error: {_scrub_secrets(str(exc))[:200]}", file=sys.stderr)
        return False, "network_error"


# ------------------------------- Auth -------------------------------
_AUTH_COOKIE = "maep_session"
_AUTH_EPHEMERAL = None
_LOGIN_FAILS = {}
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")


def _auth_secret():
    raw = os.getenv("APP_AUTH_SECRET") or os.getenv("SUPABASE_SERVICE_KEY")
    if raw:
        return hashlib.sha256(raw.encode()).digest()
    global _AUTH_EPHEMERAL
    if _AUTH_EPHEMERAL is None:
        _AUTH_EPHEMERAL = secrets.token_bytes(32)
    return _AUTH_EPHEMERAL


def _pw_hash(password):
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return "pbkdf2$200000$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(dk).decode()


def _pw_verify(password, stored):
    try:
        _, iters, salt_b64, hash_b64 = stored.split("$")
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(),
                                 base64.b64decode(salt_b64), int(iters))
        return hmac.compare_digest(base64.b64encode(dk).decode(), hash_b64)
    except Exception:
        return False


def _b64u(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64u_dec(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _make_session(email):
    payload = {"sub": email, "exp": int(time.time()) + 30 * 24 * 3600}
    part = _b64u(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(_auth_secret(), part.encode(), hashlib.sha256).digest()
    return part + "." + _b64u(sig)


def _read_session(token):
    if not token or "." not in token:
        return None
    part, sig = token.rsplit(".", 1)
    good = _b64u(hmac.new(_auth_secret(), part.encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(sig, good):
        return None
    try:
        payload = json.loads(_b64u_dec(part))
    except Exception:
        return None
    if int(payload.get("exp", 0)) < int(time.time()):
        return None
    email = payload.get("sub")
    return email if isinstance(email, str) and email else None


def _users_path():
    return _trk_data_dir() / "users.json"


def _users_load():
    try:
        return json.loads(_users_path().read_text(encoding="utf-8"))
    except Exception:
        return {}


def _users_save(store):
    path = _users_path()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(store, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def _user_get(email):
    url, _ = _sb_target()
    if not url:
        rec = _users_load().get(email)
        return {"email": email, "pass_hash": rec["pass_hash"]} if rec else None
    try:
        rows = _sb_req("GET", "app_users", params={"email": f"eq.{email}", "select": "*"})
        if not rows:
            return None
        return {"email": rows[0]["email"], "pass_hash": rows[0]["pass_hash"]}
    except Exception as exc:
        print(f"[auth] user read error: {_scrub_secrets(str(exc))[:200]}", file=sys.stderr)
        return None


def _user_create(email, pass_hash):
    url, _ = _sb_target()
    if not url:
        store = _users_load()
        store[email] = {"pass_hash": pass_hash}
        _users_save(store)
        return
    _sb_req("POST", "app_users", payload={"email": email, "pass_hash": pass_hash})


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

    def _targets_for(model_id):
        """Ordered attempts for a registry model: primary, then fallbacks.

        Each attempt is {client, model, params, retry}. Fallbacks reuse the
        same provider client — they are just other model IDs on it — so a
        busy free model (429) rolls over instead of failing the request.
        """
        entry = model_registry.get(model_id) or {}
        client, params = client_for(model_id)
        targets = [{
            "client": client,
            "model": entry.get("underlying", model_id),
            "params": params,
            "retry": bool(entry.get("retry")),
        }]
        for fb_model in entry.get("fallback_models") or []:
            targets.append({
                "client": client,
                "model": fb_model,
                "params": params,
                "retry": False,
            })
        return targets

    def _vision_targets():
        """Ordered vision attempts: NVIDIA -> GPT-4o -> Claude -> OpenRouter free."""
        candidates = [
            APP_MODELS.get("vision", "meta/llama-3.2-90b-vision-instruct"),
            "openai/gpt-4o",
            "anthropic/claude-vision",
            "openrouter/gemma-4-31b-vision-free",
        ]
        for vision_id in candidates:
            if vision_id in model_registry:
                return _targets_for(vision_id)
        return []

    def _vision_target():
        targets = _vision_targets()
        if targets:
            first = targets[0]
            return first["client"], first["model"]
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

    def _sse_stream(targets, messages, lang="en"):
        """Stream a completion, rolling over to the next target on failure.

        `targets` is an ordered list of {client, model, params, retry}
        (a single bare target dict is also accepted). When a model fails
        BEFORE producing any content — the common case: OpenRouter free
        tier answers 429 while its shared upstream pool is busy — the next
        model is tried and the user never sees the error. If every model
        fails, the client gets one short localized message instead of the
        raw provider payload.
        """
        if isinstance(targets, dict):
            targets = [targets]
        start = time.monotonic()
        emitted = False
        last_exc = None
        for target in targets:
            try:
                completion = _create_completion(
                    target["client"], target["model"], messages,
                    target["params"], retry=target.get("retry", False),
                )
                for chunk in completion:
                    if not getattr(chunk, "choices", None):
                        continue
                    choice = chunk.choices[0]
                    delta = getattr(choice, "delta", None)
                    if delta is None:
                        continue
                    content = getattr(delta, "content", None)
                    if content:
                        if not emitted:
                            emitted = True
                            ttft_ms = int((time.monotonic() - start) * 1000)
                            yield f"event: meta\ndata: {json.dumps({'ttft_ms': ttft_ms, 'model': target['model']})}\n\n"
                        yield f"data: {json.dumps({'content': content})}\n\n"
                total_ms = int((time.monotonic() - start) * 1000)
                yield f"event: done\ndata: {json.dumps({'total_ms': total_ms})}\n\n"
                return
            except Exception as exc:  # noqa: BLE001 - roll over unless already streaming
                last_exc = exc
                print(
                    f"[ai] model {target.get('model')} failed: "
                    f"{_scrub_secrets(str(exc))[:300]}",
                    file=sys.stderr,
                )
                if emitted:
                    break
        if last_exc is not None:
            yield f"event: error\ndata: {json.dumps({'message': _friendly_ai_error(last_exc, lang)})}\n\n"

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

        messages = []
        if system_content:
            messages.append({"role": "system", "content": system_content})
        messages.append({"role": "user", "content": user_prompt})

        return _sse_response(_sse_stream(_targets_for(model_id), messages, lang=lang))

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

    _PUBLIC_PREFIXES = ("/api/auth/", "/api/branding", "/api/health",
                        "/api/webhooks/")
    _PROTECTED_PREFIXES = ("/api/chat", "/api/models", "/api/tracking/",
                           "/api/sales")

    @app.middleware("http")
    async def _auth_gate(request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in _PROTECTED_PREFIXES) and not any(
                path.startswith(p) for p in _PUBLIC_PREFIXES):
            email = _read_session(request.cookies.get(_AUTH_COOKIE) or "")
            if not email:
                return JSONResponse({"error": "unauthorized"}, status_code=401)
            request.state.user_email = email
        return await call_next(request)

    def _session_cookie(resp, email):
        resp.set_cookie(_AUTH_COOKIE, _make_session(email),
                        max_age=30 * 24 * 3600, path="/", httponly=True,
                        samesite="lax",
                        secure=bool(os.getenv("VERCEL")))
        return resp

    def _valid_credentials(body):
        email = str(body.get("email") or "").strip().lower()[:200]
        password = str(body.get("password") or "")
        if not _EMAIL_RE.match(email):
            raise HTTPException(400, "invalid_email")
        if len(password) < 8 or len(password) > 200:
            raise HTTPException(400, "weak_password")
        return email, password

    @app.post("/api/auth/register")
    async def auth_register(request: Request):
        if os.getenv("APP_REGISTRATION", "open").lower() == "closed":
            raise HTTPException(403, "registration_closed")
        email, password = _valid_credentials(await request.json())
        if _user_get(email):
            raise HTTPException(409, "account_exists")
        _user_create(email, _pw_hash(password))
        return _session_cookie(JSONResponse({"ok": True, "email": email}), email)

    @app.post("/api/auth/login")
    async def auth_login(request: Request):
        body = await request.json()
        email = str(body.get("email") or "").strip().lower()[:200]
        password = str(body.get("password") or "")
        now = int(time.time())
        fails = [t for t in _LOGIN_FAILS.get(email, []) if now - t < 600]
        if len(fails) >= 8:
            raise HTTPException(429, "too_many_attempts")
        user = _user_get(email) if _EMAIL_RE.match(email) else None
        if not user or not _pw_verify(password, user["pass_hash"]):
            _LOGIN_FAILS[email] = fails + [now]
            raise HTTPException(401, "invalid_credentials")
        _LOGIN_FAILS.pop(email, None)
        return _session_cookie(JSONResponse({"ok": True, "email": email}), email)

    @app.post("/api/auth/logout")
    async def auth_logout():
        resp = JSONResponse({"ok": True})
        resp.delete_cookie(_AUTH_COOKIE, path="/")
        return resp

    @app.get("/api/auth/me")
    async def auth_me(request: Request):
        email = _read_session(request.cookies.get(_AUTH_COOKIE) or "")
        if not email:
            raise HTTPException(401, "unauthorized")
        return {"email": email}


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

        return _sse_response(_sse_stream(_targets_for(model), messages, lang=lang))

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
        vision_targets = _vision_targets()
        if not vision_targets:
            raise HTTPException(503, _msg(lang, "vision_not_configured"))

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text", "text": _msg(lang, "analyze_image_prompt")},
            ]},
        ]

        return _sse_response(_sse_stream(vision_targets, messages, lang=lang))

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

        vision_targets = _vision_targets()
        if not vision_targets:
            raise HTTPException(503, _msg(lang, "vision_not_configured"))

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text", "text": _msg(lang, "analyze_screenshot_prompt")},
            ]},
        ]

        return _sse_response(_sse_stream(vision_targets, messages, lang=lang))

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

    # ----------------------------- Tracking -----------------------------
    def _trk_record(key):
        return _store_get(key)

    def _trk_public_view(rec):
        if not rec or not rec.get("config"):
            return {"configured": False, "has_token": False}
        cfg = rec["config"]
        return {
            "configured": True,
            "pixel_id": cfg.get("pixel_id", ""),
            "domain": cfg.get("domain", ""),
            "test_code": cfg.get("test_code", ""),
            "events": cfg.get("events", []),
            "has_token": bool(cfg.get("token")),
            "last_test_ok": rec.get("last_test_ok"),
        }

    @app.post("/api/tracking/config")
    async def tracking_save_config(request: Request):
        body = await request.json()
        key = _trk_clean(body.get("key"), 64).lower()
        if not _TRK_KEY_RE.match(key):
            raise HTTPException(400, "invalid_key")
        pixel = re.sub(r"\D", "", _trk_clean(body.get("pixel_id"), 32))
        if not _TRK_PIXEL_RE.match(pixel):
            raise HTTPException(400, "invalid_pixel")
        domain = _trk_clean(body.get("domain"), 120).lower()
        domain = re.sub(r"^https?://", "", domain).split("/")[0]
        if domain and not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", domain):
            raise HTTPException(400, "invalid_domain")
        events = [e for e in (body.get("events") or []) if e in _TRK_EVENTS] or ["PageView"]
        rec = _store_get(key) or {"config": {}, "sales": []}
        cfg = rec.get("config") or {}
        token_in = str(body.get("token") or "").strip()
        if token_in:
            cfg["token"] = token_in[:512]
        cfg.update({"pixel_id": pixel, "domain": domain,
                    "test_code": _trk_clean(body.get("test_code"), 64).upper(),
                    "events": events})
        rec["config"] = cfg
        _store_put_config(key, cfg, rec.get("last_test_ok"))
        return {"ok": True, **_trk_public_view(rec)}

    @app.get("/api/tracking/config")
    async def tracking_get_config(key: str = ""):
        key = _trk_clean(key, 64).lower()
        if not _TRK_KEY_RE.match(key):
            return {"configured": False, "has_token": False}
        return _trk_public_view(_trk_record(key))

    @app.post("/api/tracking/test")
    async def tracking_test(request: Request):
        body = await request.json()
        key = _trk_clean(body.get("key"), 64).lower()
        rec = _trk_record(key) if _TRK_KEY_RE.match(key) else None
        if not rec or not rec.get("config"):
            raise HTTPException(400, "not_configured")
        ok, detail = _capi_test(rec["config"])
        _store_put_config(key, rec["config"], ok)
        return {"ok": ok, "detail": detail}

    @app.post("/api/tracking/test-event")
    async def tracking_test_event(request: Request):
        body = await request.json()
        key = _trk_clean(body.get("key"), 64).lower()
        rec = _trk_record(key) if _TRK_KEY_RE.match(key) else None
        if not rec or not rec.get("config"):
            raise HTTPException(400, "not_configured")
        cfg = rec["config"]
        if not cfg.get("test_code"):
            raise HTTPException(400, "test_code_required")
        event_id = "test-" + uuid.uuid4().hex[:24]
        ok, detail = _capi_send(cfg, "PageView", event_id,
                                pii={"email": "test@example.com", "name": "Test"},
                                test_code=cfg["test_code"])
        return {"ok": ok, "detail": detail, "event_id": event_id}

    @app.post("/api/webhooks/sales/{key}")
    async def tracking_sales_webhook(key: str, request: Request):
        key = _trk_clean(key, 64).lower()
        if not _TRK_KEY_RE.match(key):
            raise HTTPException(404, "not_found")
        raw = await request.body()
        if len(raw) > 262144:
            raise HTTPException(413, "payload_too_large")
        try:
            body = json.loads(raw.decode("utf-8", "replace"))
        except Exception:
            raise HTTPException(400, "invalid_json")
        sale = _trk_extract_sale(body)
        if not sale or sale.get("amount") is None:
            raise HTTPException(400, "unrecognized_payload")
        rec = _store_get(key) or {"config": {}, "sales": []}
        cfg = rec.get("config") or {}
        event_name = _trk_sale_event(sale["status"], sale["method"])
        capi_status = "skipped"
        event_id = "sale-" + uuid.uuid4().hex[:24]
        if event_name and cfg.get("pixel_id") and cfg.get("token"):
            ok, detail = _capi_send(
                cfg, event_name, event_id, value=sale["amount"], currency=sale["currency"],
                pii=sale.get("_pii") or {},
                utms={k: sale.get(k) for k in ("utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content")})
            capi_status = "sent" if ok else f"error:{detail}"
        elif event_name:
            capi_status = "no_credentials"
        record = {
            "id": event_id, "ts": int(time.time()), "platform": sale["platform"],
            "method": sale["method"], "status": sale["status"],
            "amount": sale["amount"], "currency": sale["currency"],
            "utm_source": sale.get("utm_source", ""), "utm_medium": sale.get("utm_medium", ""),
            "utm_campaign": sale.get("utm_campaign", ""), "utm_term": sale.get("utm_term", ""),
            "utm_content": sale.get("utm_content", ""),
            "has_fbp": bool((sale.get("_pii") or {}).get("fbp")),
            "has_fbc": bool((sale.get("_pii") or {}).get("fbc")),
            "capi_event": event_name, "capi_status": capi_status, "capi_event_id": event_id,
        }
        _store_add_sale(key, record)
        return {"ok": True, "sale_id": event_id, "capi_event": event_name, "capi_status": capi_status}

    @app.get("/api/sales")
    async def tracking_list_sales(key: str = "", method: str = ""):
        key = _trk_clean(key, 64).lower()
        rec = _trk_record(key) if _TRK_KEY_RE.match(key) else None
        sales = list((rec or {}).get("sales") or [])
        if method in ("pix", "boleto", "card", "other"):
            sales = [s for s in sales if s.get("method") == method]
        sales.sort(key=lambda s: s.get("ts", 0), reverse=True)
        return {"sales": sales[:200], "total": len(sales)}

    return _strip_vercel_prefix(app)
