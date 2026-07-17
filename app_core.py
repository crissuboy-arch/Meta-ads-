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
    list_configs,
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
                new_prefix = prefix + "/" + entry.name if prefix else entry.name
                _walk_and_load(entry, new_prefix)

    _walk_and_load(skills_dir)
    return skills


def _build_registry(skills=None):
    if skills is None:
        skills = {}
    default_key = os.getenv("NVIDIA_API_KEY")
    if not default_key:
        raise RuntimeError(
            "NVIDIA_API_KEY nao encontrada. Local: confira o .env. "
            "Na Vercel: importe o .env.vercel em Project Settings -> Environment Variables."
        )
    registry = {
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

    for skill_id, skill in skills.items():
        registry[skill_id] = {
            "label": skill["label"],
            "provider": "Expert",
            "category": "llm",
            "api_key": os.getenv(f"NVIDIA_API_KEY_{skill_id.upper().replace('-', '_')}", default_key),
            "params": {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096},
            "underlying": APP_MODELS.get("expert_underlying", DEFAULT_MODEL),
            "skill_content": skill["content"],
        }

    return registry


def create_app():
    skills = _load_skills()
    model_registry = _build_registry(skills)
    default_key = os.getenv("NVIDIA_API_KEY")
    clients = {}

    def client_for(model_id):
        entry = model_registry.get(model_id)
        key = entry["api_key"] if entry else default_key
        params = entry["params"] if entry else {"temperature": 0.7, "top_p": 0.95, "max_tokens": 4096}
        if key not in clients:
            clients[key] = OpenAI(base_url=BASE_URL, api_key=key, timeout=REQUEST_TIMEOUT)
        return clients[key], params

    def _sse_stream(client, model, messages, params):
        start = time.monotonic()
        first_token_at = None
        try:
            completion = client.chat.completions.create(
                model=model, messages=messages, stream=True, **params,
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

    def _stream_analysis(user_prompt: str, model_id: str = None):
        if model_id is None:
            model_id = CONFIG.get("app_id", "pro")
        entry = model_registry.get(model_id)
        if not entry:
            return JSONResponse({"error": "Modelo nao encontrado"}, status_code=500)

        skill_content = entry.get("skill_content", "")
        underlying = entry.get("underlying", model_id)
        client, params = client_for(model_id)

        messages = [
            {"role": "system", "content": skill_content},
            {"role": "user", "content": user_prompt},
        ]

        return _sse_response(_sse_stream(client, underlying, messages, params))

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

    def _fetch_and_clean_url(url: str) -> dict:
        if _requests is None:
            raise HTTPException(500, "Biblioteca 'requests' nao instalada. Execute: pip install requests beautifulsoup4")
        if BeautifulSoup is None:
            raise HTTPException(500, "Biblioteca 'beautifulsoup4' nao instalada. Execute: pip install beautifulsoup4")

        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname or ""

        if parsed.scheme == "file":
            raise HTTPException(400, "URLs de arquivo nao sao permitidas")
        if hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            raise HTTPException(400, "URLs locais nao sao permitidas")
        if hostname.endswith(".local") or hostname.endswith(".internal"):
            raise HTTPException(400, "URLs internas nao sao permitidas")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        try:
            resp = _requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            resp.raise_for_status()
        except _requests.Timeout:
            raise HTTPException(408, "A pagina demorou muito para responder. Tente novamente.")
        except _requests.HTTPError as e:
            code = e.response.status_code
            friendly = {403: "Acesso negado (403). A pagina pode exigir login.", 404: "Pagina nao encontrada (404)."}
            raise HTTPException(code, friendly.get(code, f"Erro HTTP {code} ao acessar a pagina."))
        except _requests.ConnectionError:
            raise HTTPException(502, "Nao foi possivel conectar ao servidor. Verifique a URL.")
        except _requests.RequestException as e:
            raise HTTPException(400, f"Erro ao acessar a URL: {str(e)[:120]}")

        ct = resp.headers.get("content-type", "")
        if "text/html" not in ct and "application/xhtml" not in ct:
            raise HTTPException(400, "A URL nao retornou uma pagina HTML.")

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
        return JSONResponse({"status": "ok", "models": list(model_registry.keys())})

    @app.get("/api/branding")
    def branding(app_id: str = None):
        if app_id:
            try:
                cfg = get_config(app_id)
                reload_config()
                return JSONResponse(cfg)
            except FileNotFoundError:
                raise HTTPException(404, f"Aplicativo '{app_id}' nao encontrado.")
        return JSONResponse(CONFIG)

    @app.get("/api/configs")
    def available_configs():
        return JSONResponse(list_configs())

    @app.post("/api/chat")
    async def chat(request: Request):
        body = await request.json()
        messages = body.get("messages", [])
        model = (body.get("model") or DEFAULT_MODEL).strip()

        entry = model_registry.get(model, {})
        skill_content = entry.get("skill_content")
        if skill_content:
            messages = [{"role": "system", "content": skill_content}] + messages

        client, params = client_for(model)
        api_model = entry.get("underlying", model)

        return _sse_response(_sse_stream(client, api_model, messages, params))

    @app.post("/api/upload-image")
    async def upload_image(file: UploadFile = File(...)):
        if not UPLOADS.get("image", True):
            raise HTTPException(400, "Upload de imagem nao habilitado para este aplicativo.")

        valid_ext = {"jpg", "jpeg", "png", "webp"}
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in valid_ext:
            raise HTTPException(400, "Formato inv\u00e1lido. Aceitos: JPG, JPEG, PNG, WEBP")

        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(400, "Arquivo muito grande. M\u00e1ximo: 10MB")

        b64 = base64.b64encode(contents).decode("utf-8")
        mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
        mime = mime_map.get(ext, "image/jpeg")

        system_prompt = SYSTEM_PROMPTS.get("image", "Analise esta imagem.")
        vision_key = os.getenv("NVIDIA_API_KEY_VISION", default_key)
        vision_client = OpenAI(base_url=BASE_URL, api_key=vision_key, timeout=REQUEST_TIMEOUT)
        vision_model = APP_MODELS.get("vision", "meta/llama-3.2-90b-vision-instruct")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text", "text": "Analise esta imagem de produto ou an\u00fancio detalhadamente."},
            ]},
        ]

        vision_params = {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048}
        return _sse_response(_sse_stream(vision_client, vision_model, messages, vision_params))

    @app.post("/api/upload-pdf")
    async def upload_pdf(file: UploadFile = File(...)):
        if not UPLOADS.get("pdf", True):
            raise HTTPException(400, "Upload de PDF nao habilitado para este aplicativo.")

        if PdfReader is None:
            raise HTTPException(500, "Biblioteca 'pypdf' nao instalada. Execute: pip install pypdf")

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(400, "Formato inv\u00e1lido. Aceito apenas PDF.")
        contents = await file.read()
        if len(contents) > 20 * 1024 * 1024:
            raise HTTPException(400, "Arquivo muito grande. M\u00e1ximo: 20MB")

        safe_name = re.sub(r"[^\w\.\-]", "_", file.filename)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        try:
            tmp.write(contents)
            tmp.close()
            reader = PdfReader(tmp.name)
            text_parts = [p.extract_text() or "" for p in reader.pages]
            full_text = "\n".join(text_parts).strip()
            if len(full_text) < 50:
                return JSONResponse({"error": "Este PDF parece ser digitalizado e nao contem texto extraivel. Tente fazer upload de uma imagem do documento."}, status_code=400)
            if len(full_text) > 15000:
                full_text = full_text[:15000] + "\n[... conteudo truncado por limite de tamanho]"
        finally:
            os.unlink(tmp.name)

        instruction = SYSTEM_PROMPTS.get("pdf", "Analise o documento.")

        return _stream_analysis(f"{instruction}\n\nConteudo extraido do PDF ({safe_name}):\n\n{full_text}")

    @app.post("/api/upload-screenshot")
    async def upload_screenshot(file: UploadFile = File(...)):
        if not UPLOADS.get("screenshot", True):
            raise HTTPException(400, "Upload de screenshot nao habilitado para este aplicativo.")

        valid_ext = {"jpg", "jpeg", "png", "webp"}
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if ext not in valid_ext:
            raise HTTPException(400, "Formato invalido. Aceitos: JPG, JPEG, PNG, WEBP")
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(400, "Arquivo muito grande. Maximo: 10MB")

        b64 = base64.b64encode(contents).decode("utf-8")
        mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
        mime = mime_map.get(ext, "image/jpeg")

        system_prompt = SYSTEM_PROMPTS.get("screenshot", "")
        if not system_prompt:
            raise HTTPException(400, "Upload de screenshot nao disponivel para este aplicativo.")

        vision_key = os.getenv("NVIDIA_API_KEY_VISION", default_key)
        vision_client = OpenAI(base_url=BASE_URL, api_key=vision_key, timeout=REQUEST_TIMEOUT)
        vision_model = APP_MODELS.get("vision", "meta/llama-3.2-90b-vision-instruct")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text", "text": "Analise esta captura de tela detalhadamente."},
            ]},
        ]

        vision_params = {"temperature": 0.7, "top_p": 0.95, "max_tokens": 2048}
        return _sse_response(_sse_stream(vision_client, vision_model, messages, vision_params))

    @app.post("/api/analyze-url")
    async def analyze_url(request: Request):
        if not UPLOADS.get("url", True):
            raise HTTPException(400, "Analise de URL nao habilitada para este aplicativo.")

        body = await request.json()
        url = body.get("url", "").strip()
        analysis_type = body.get("type", "lp")

        if not url:
            raise HTTPException(400, "URL nao informada.")
        if not url.startswith("http://") and not url.startswith("https://"):
            raise HTTPException(400, "URL deve comecar com http:// ou https://")

        page_data = _fetch_and_clean_url(url)

        platform = _detect_platform(url)
        product_types = _detect_product_type(url + " " + page_data["title"] + " " + page_data["content"][:3000])
        platform_info = f"Plataforma detectada: {platform}\n" if platform else ""
        product_info = f"Tipo de produto detectado: {', '.join(product_types)}\n" if product_types else ""

        url_prompts = SYSTEM_PROMPTS.get("url", {})
        instruction = url_prompts.get(analysis_type) or url_prompts.get("lp", "Analise esta pagina.")
        user_content = (
            f"{instruction}\n\n"
            f"URL analisada: {url}\n"
            f"{platform_info}"
            f"{product_info}"
            f"Titulo da pagina: {page_data['title']}\n"
            f"Meta Description: {page_data['description']}\n\n"
            f"Conteudo extraido:\n{page_data['content']}"
        )
        return _stream_analysis(user_content)

    @app.post("/api/embeddings")
    async def embeddings(request: Request):
        body = await request.json()
        text = body.get("input", body.get("text", ""))
        model = body.get("model", "nvidia/nv-embedqa-e5-v5")
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

    return app
