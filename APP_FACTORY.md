# ForgeHub AI - App Factory

Arquitetura modular para criar microapps com IA em **menos de 2 minutos**.

## Filosofia

> **Zero código duplicado.** Cada novo app = 1 arquivo JSON + 1 arquivo Markdown.
> Backend e frontend s\u00e3o 100% gen\u00e9ricos e reutiliz\u00e1veis.

## Estrutura de Diret\u00f3rios

```
/
+-- configs/           JSON de configuracao de cada app
|   +-- meta-ads.json
|   +-- google-ads.json
|   +-- seu-app.json       <-- CRIE ESTE
+-- skills/            System prompt de cada especialista
|   +-- pro.md
|   +-- seu-app.md          <-- CRIE ESTE
+-- assets/            Recursos especificos por app (icones, logos, etc)
|   +-- seu-app/
+-- apps/              (reservado) Overrides especificos por app
+-- shared/            Componentes compartilhados entre apps
+-- templates/         Documentacao de template
+-- static/
|   +-- index.html     Frontend 100% dinamico (NAO precisa alterar)
+-- app_core.py        Backend generico (NAO precisa alterar)
+-- config.py          Multi-app loader com cache
+-- create_app.py      CLI para gerar novos apps
```

## Como criar um novo app em <2 minutos

### Via CLI (recomendado)

```bash
# App novo com template padrao
python create_app.py relacionamento

# App novo baseado em um app existente
python create_app.py nutricao --template copywriter

# Listar apps disponiveis
python create_app.py list
```

O comando cria automaticamente:

| Arquivo | Conteudo |
|---------|----------|
| `configs/relacionamento.json` | Config completa com branding, prompts, menus, toolse |
| `skills/relacionamento.md` | System prompt do especialista |
| `assets/relacionamento/` | Diretorio de recursos |

### Manual

```bash
# 1. Copiar config de referencia
cp configs/meta-ads.json configs/meu-app.json

# 2. Editar configs/meu-app.json
#    - app_id, branding, colors, skill, prompts, tools, sidebar

# 3. Criar skill
cp skills/pro.md skills/meu-app.md

# 4. Executar
export APP_ID=meu-app
uvicorn app_core:create_app --reload
```

## App Switcher (Multi-app)

O frontend possui um **seletor de apps** no topo da sidebar.

- Ao trocar de app, a interface inteira se reconfigure:
  - Branding (nome, logo, empresa)
  - Cores (primaria, secundaria, fundo)
  - Sidebar (menus, categorias)
  - Ferramentas, imports, niches
  - Prompts (comportamento do chat)
  - Hero, dashboard metrics
  - Uploads habilitados
- Tudo é carregado via `/api/branding?app_id=X`
- Nenhum nome fica fixo no frontend

## API de Configuracoes

| Endpoint | Descricao |
|----------|-----------|
| `GET /api/branding` | Config do app ativo (definido por APP_ID) |
| `GET /api/branding?app_id=X` | Config de qualquer app |
| `GET /api/configs` | Lista todos os apps disponiveis |

## Variaveis de Ambiente

| Variavel | Descricao | Padrao |
|----------|-----------|--------|
| `APP_ID` | App ativo na inicializacao | `meta-ads` |
| `NVIDIA_API_KEY` | Chave principal da API NVIDIA | (obrigatorio) |

## Checklist para criar um app completo

- [ ] `python create_app.py meu-app` (ou copiar manualmente)
- [ ] Editar `configs/meu-app.json`:
  - [ ] `branding.app_name` e `branding.short_name`
  - [ ] `colors` (paleta de cores)
  - [ ] `hero.title`, `hero.subtitle`
  - [ ] `sidebar` (menus laterais)
  - [ ] `tools` (ferramentas principais)
  - [ ] `imports` (tipos de upload)
  - [ ] `prompts` (comportamento consultivo para cada ferramenta)
  - [ ] `system_prompts` (analise de imagem, PDF, URL)
  - [ ] `action_buttons` (acoes pos-analise)
  - [ ] `uploads` (quais uploads habilitar)
  - [ ] `niches` (nichos de mercado, se aplicavel)
- [ ] Editar `skills/meu-app.md` (system prompt do especialista)
- [ ] Testar com `export APP_ID=meu-app && uvicorn app_core:create_app --reload`
- [ ] Verificar se o frontend carregou corretamente

## Pronto.

Seu novo microapp esta rodando com IA, uploads, analise de URL e interface premium — sem escrever uma linha de backend ou frontend.
