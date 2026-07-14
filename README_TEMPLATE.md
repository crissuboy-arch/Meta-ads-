# ForgeHub AI - Template Base v1.0

Esta é a **base oficial** de todos os aplicativos da suíte ForgeHub AI.

## 🧠 Arquitetura

```
/
├── configs/          # Configurações de cada aplicativo (JSON)
│   ├── meta-ads.json     # Meta Ads Expert PRO (referência)
│   ├── google-ads.json   # Google Ads Expert PRO
│   ├── tiktok-ads.json   # TikTok Ads Expert PRO
│   ├── landing-pages.json
│   ├── copywriter.json
│   ├── seo.json
│   ├── crm.json
│   └── analytics.json
├── skills/           # System prompts dos especialistas (.md)
│   ├── pro.md            # Meta Ads Expert
│   ├── meta-ads.md       # Meta Ads base
│   └── ...
├── static/           # Frontend (NÃO precisa modificar)
│   └── index.html
├── templates/        # Documentação de template
│   └── README.md
├── app_core.py       # Backend (NÃO precisa modificar)
├── config.py         # Carregador de configurações JSON
└── .env              # Chaves de API
```

## 🚀 Como criar um novo aplicativo em <5 minutos

### 1. Criar o arquivo de configuração

```bash
cp configs/meta-ads.json configs/meu-app.json
```

### 2. Personalizar

Edite `configs/meu-app.json` alterando **apenas**:

| Campo | O que muda |
|-------|-----------|
| `app_id` | Identificador único (ex: `"meu-app"`) |
| `branding.app_name` | Nome do aplicativo |
| `branding.short_name` | Versão curta do nome |
| `branding.assistant_name` | Nome do assistente no chat |
| `colors.primary` | Cor principal (hex) |
| `colors.secondary` | Cor secundária (hex) |
| `skill` | Arquivo .md do especialista (ex: `"meu-app.md"`) |
| `hero.title` | Título da página inicial |
| `hero.subtitle` | Subtítulo |
| `sidebar` | Itens do menu lateral |
| `tools` | Ferramentas principais |
| `imports` | Tipos de upload disponíveis |
| `niches` | Nichos de mercado |
| `prompts` | Comportamento consultivo do chat |
| `system_prompts` | Prompts para análises (imagem, PDF, URL) |
| `action_buttons` | Botões rápidos pós-análise |
| `uploads` | Quais uploads habilitar |

### 3. Criar o system prompt do especialista

```bash
cp skills/pro.md skills/meu-app.md
```

Edite `skills/meu-app.md` com o system prompt do seu especialista.

### 4. Executar

```bash
export APP_ID=meu-app
python -m uvicorn app_core:create_app --reload
```

O frontend carregará automaticamente todas as configurações.

## ✅ O que NÃO precisa ser alterado

- `app_core.py` — backend genérico, lê tudo do JSON
- `config.py` — loader automático baseado em `APP_ID`
- `static/index.html` — renderiza dinamicamente do config
- Nenhuma linha de código precisa ser escrita

## 📦 Configurações disponíveis (built-in)

| APP_ID | Aplicativo |
|--------|-----------|
| `meta-ads` | Meta Ads Expert PRO |
| `google-ads` | Google Ads Expert PRO |
| `tiktok-ads` | TikTok Ads Expert PRO |
| `landing-pages` | Landing Pages Expert PRO |
| `copywriter` | Copywriter Expert PRO |
| `seo` | SEO Expert PRO |
| `crm` | CRM & Vendas Expert PRO |
| `analytics` | Analytics Expert PRO |

## 📋 Estrutura do JSON de configuração

```json
{
  "app_id": "meu-app",
  "branding": { "app_name": "...", "colors": "...", ... },
  "colors": { "primary": "#...", ... },
  "models": { "default": "...", "vision": "...", "expert_underlying": "..." },
  "skill": "meu-app.md",
  "hero": { "title": "...", "highlight": "...", "subtitle": "...", "floats": [...] },
  "dashboard_metrics": [...],
  "sidebar": { "categories": [...], "items": {...} },
  "tools": [...],
  "imports": [...],
  "niches": [...],
  "action_buttons": [...],
  "uploads": { "image": true, "pdf": true, "screenshot": false, "url": true },
  "url_analysis": { "types": [...], "platform_patterns": [...], "product_type_keywords": {...} },
  "system_prompts": { "image": "...", "pdf": "...", "screenshot": "...", "url": { "lp": "...", ... } },
  "prompts": { "ferramenta-id": "prompt consultivo...", ... }
}
```

## 🔄 Alternar entre aplicativos

```bash
# Meta Ads
export APP_ID=meta-ads && python -m uvicorn app_core:create_app --reload

# Google Ads  
export APP_ID=google-ads && python -m uvicorn app_core:create_app --reload

# TikTok Ads
export APP_ID=tiktok-ads && python -m uvicorn app_core:create_app --reload
```

## 📌 Princípios da Base Template

1. **Zero duplicação de código** — backend e frontend são genéricos
2. **Tudo configurável via JSON** — branding, prompts, cores, menus, uploads
3. **Separação total** — config, skill, código e dados nunca se misturam
4. **Pronto para deploy** — qualquer app criado roda imediatamente
5. **Escala infinita** — novos apps = novos .json + .md
