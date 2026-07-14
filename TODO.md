# TODO

## Pendentes para v1.1

### Criticos

- [ ] `list_configs()` usa `except Exception: pass` — engole erros silenciosamente
- [ ] `upload_image` e `upload_screenshot` compartilham `_read_upload_image()` mas ainda tem duplicacao de setup do vision_client
- [ ] `reload_config()` chamado em `/api/branding` anula proposito do cache
- [ ] Nenhuma validacao de schema JSON na inicializacao

### Seguranca

- [ ] SSRF protection nao cobre RFC 1918 (10.x, 172.16-31.x, 192.168.x), link-local (169.254.x), IPv4-mapped
- [ ] `_requests.get()` com `allow_redirects=True` sem limite de redirects
- [ ] API keys podem ser `None` se env var nao existir (gera erro obscuro no OpenAI client)

### Performance

- [ ] `_requests.get()` (sync) dentro de `async def analyze_url` — bloqueia event loop
- [ ] `embeddings.create()` (sync) dentro de `async def embeddings`
- [ ] Nenhum cache de modelo — `client_for()` cria novo client a cada chamada

### Codigo

- [ ] `event_stream` generator extraido para `_sse_stream()` mas visao ainda usa hardcoded vision_params
- [ ] Model registry ainda definido em `_build_registry()` dentro de `create_app()` — idealmente extrair para modulo separado
- [ ] `api/chat.py` e `api/models.py` — endpoints serverless Vercel com model registry duplicado
- [ ] `server.py` — importa mas nao usa nada de app_core explicitamente (wrapper Vercel)
- [ ] Nomes de arquivo inconsistentes: `README_TEMPLATE.md` vs `APP_FACTORY.md` (mesmo proposito)

### Frontend

- [ ] Parsing SSE duplicado 5x em `streamChat()`, `handleImageUpload()`, `handlePDFUpload()`, `handleScreenshotUpload()`, `handleURLAnalysis()` — extrair funcao compartilhada
- [ ] Post-stream rendering (~15 linhas) duplicado 4x nos handlers de upload
- [ ] Progresso indeterministico (`Math.random()`) em vez de progresso real
- [ ] File size limits hardcoded (10/20MB) em vez de vir da config
- [ ] Acessibilidade: botoes sem `aria-label`, textarea sem `<label>`, sem `aria-live` no log
