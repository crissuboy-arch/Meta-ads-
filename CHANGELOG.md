# Changelog

## v1.0 (2026-07-14)

### Nova Arquitetura — App Factory

- **Multi-app**: Configuracao por JSON em `configs/<app_id>.json`. 8 apps inclusos.
- **App Switcher**: Seletor de apps no frontend. Troca branding, cores, ferramentas e prompts em tempo real.
- **CLI Generator**: `python create_app.py <nome>` cria um novo app em <2 segundos.
- **Skill System**: System prompts modulares em `skills/<app_id>.md`.
- **`config.py`**: Loader generico com cache (`get_config`, `reload_config`, `list_configs`).
- **`app_core.py`**: Single backend generico. Rotas `/api/branding?app_id=X` e `/api/configs`.
- **`index.html`**: Frontend 100% dinamico. Zero nomes hardcoded. Renderiza sidebar, tools, imports, niches, hero via JSON.

### Novos Arquivos

| Arquivo | Proposito |
|---------|-----------|
| `configs/*.json` (8) | Configuracoes de cada app |
| `skills/*.md` (8) | System prompts de cada especialista |
| `templates/` | Documentacao de template |
| `create_app.py` | CLI para gerar novos apps |
| `APP_FACTORY.md` | Documentacao da arquitetura App Factory |
| `ROADMAP.md` | Roadmap do projeto |
| `TODO.md` | Tarefas pendentes |
| `VERSION.md` | Versionamento |

### Apps Inclusos

- Meta Ads Expert PRO (app padrao)
- Google Ads Expert PRO
- TikTok Ads Expert PRO
- Landing Pages Expert PRO
- Copywriter Expert PRO
- SEO Expert PRO
- CRM & Vendas Expert PRO
- Analytics Expert PRO

### Melhorias Tecnicas

- `_sse_stream()` — generator unificado de streaming SSE (removeu 4 copias identicas)
- `applyConfig()` — funcao compartilhada entre `boot()` e `selectApp()` (removeu ~50 linhas duplicadas)
- Imports mortos removidos de `app_core.py` (10 imports nao utilizados + 2 duplicatas)
- Imports mortos removidos de `create_app.py` (`shutil`, `datetime`)
- CSS morto removido (`.skeleton`, `.analysis-*`, `.result-score-ring`, `@keyframes scaleIn`)
- HTML morto removido (`#exportBtn`)
- `__pycache__` limpo

### Corrigido

- `load_config` import quebrado em `app_core.py` (funcao nao existia em config.py)
- Upload de imagem e screenshot agora compartilham `_read_upload_image()`
- Model registry consolidado (antes duplicado em 3 arquivos diferentes)

### Estrutura de Diretorios

```
/
+-- configs/       JSON de configuracao
+-- skills/        System prompts
+-- assets/        Recursos por app
+-- apps/          (reservado)
+-- shared/        (reservado)
+-- templates/     Documentacao
+-- static/        Frontend unico
+-- create_app.py  CLI generator
+-- config.py      Multi-app loader
+-- app_core.py    Backend generico
```
