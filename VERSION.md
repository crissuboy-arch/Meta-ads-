# Versao

**Meta Ads Expert PRO v1.0** — 2026-07-14

Detalhes tecnicos:

| Atributo | Valor |
|----------|-------|
| Versao | 1.0.0 |
| Release | stable |
| App padrao | Meta Ads Expert PRO |
| Total de apps | 8 |
| Engine | NVIDIA NIM (API) |
| Modelo padrao | meta/llama-3.1-70b-instruct |
| Backend | Python 3.12 + FastAPI |
| Frontend | HTML/CSS/JS vanilla |
| Deploy | Vercel (serverless) |
| CLI | `create_app.py` |

### Compatibilidade

- Python >= 3.10
- Dependencias: `openai`, `fastapi`, `uvicorn`, `python-dotenv`, `requests`, `beautifulsoup4`, `pypdf`
- Variaveis de ambiente obrigatorias: `NVIDIA_API_KEY`
- Variaveis de ambiente opcionais: `APP_ID`, `NVIDIA_API_KEY_*`

### Arquitetura

```
request -> FastAPI -> config.py (cache) -> JSON config -> app_core.py -> NVIDIA NIM API
                                                 -> static/index.html (dinamico)
```
