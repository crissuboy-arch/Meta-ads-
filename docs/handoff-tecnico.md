# Handoff técnico — consolidação das Fases A–H

**Entrega definitiva de referência para o Codex aplicar o redesign visual.**
**Não é uma release comercial** — a release comercial fica para depois dessa
revisão e do redesign.

- **Branch:** `main`
- **Commit final:** `933b7f977c0dbb1fb0dba84a2e541433ed6da4c9`
- **Checkpoint de segurança (antes da consolidação):** tag `checkpoint-pre-consolidacao-fases-a-h`
  (aponta para `4d73dd7`, o estado da `main` antes de qualquer merge desta rodada —
  use `git reset --hard checkpoint-pre-consolidacao-fases-a-h` se precisar desfazer tudo).
- **PRs consolidados:** #7, #8, #9, #10, #11, #12 e a branch `fase-g-pwa-instalador`
  (G+H), nessa ordem, cada um com merge commit próprio na `main`.

## Resultado dos testes

```
python -m pytest -q
...................................................  [100%]
51 passed in ~4.5s
```

Rodado após cada merge individual (não só no final) — 23→26→29→36→41→46→51
testes, crescendo a cada fase, sem nenhuma regressão em nenhum ponto.
`pytest.ini` já ignora os 2 scripts manuais pré-existentes (`test_api.py`,
`test_athena_integration.py`) que não são testes pytest.

CI real no GitHub Actions confirmado verde no commit final (workflow "Tests").
Build do instalador desktop (Tauri) testado na prática via tag temporária →
sucesso real em `windows-latest` e `macos-latest` (não é suposição).

Deploy automático confirmado: todo push na `main` dispara deploy de produção
na Vercel (dois projetos ligados ao repo: `meta-ads` e `meta-ads-unmc`) — os
dois deploys do commit final (`933b7f9`) terminaram com `state: success`.

## Integrações realmente verificadas (com evidência, não suposição)

| Integração | Como foi verificada |
|---|---|
| Hub de IA (OpenAI/Gemini/OpenRouter/Anthropic) | Teste real de HTTP mockado por provedor + endpoint `/api/providers/*` de ponta a ponta |
| Meta Ads (insights, CPA/CPC/CPM/frequência) | `/api/ads/insights` testado de ponta a ponta (FastAPI TestClient) |
| Criação de campanha/conjunto (sempre pausado) | `/api/ads/wizard/call` testado de ponta a ponta, incluindo o teto `MAX_DAILY_BUDGET_CENTS` e a trava `WRITE_ACTIONS_ENABLED` |
| Calculadora financeira | Funções puras testadas + endpoint `/api/finance/calc` |
| PWA (manifest, service worker, ícones) | 5 testes reais, incluindo verificação da assinatura binária do PNG |
| Instalador desktop (Tauri) | Build real no GitHub Actions (Windows + macOS), não só config escrita |
| CI (`ci.yml`) | Rodou de verdade no Actions, conclusion `success` |

## Supabase — migrações aplicadas e confirmadas ✅

Projeto: **Meta ads** (`wsdtiwdnbmijxiqlhasp`, status `ACTIVE_HEALTHY`).
Confirmado via consulta SQL real (2026-11-25): `ai_providers.calls_count`
(integer), `ai_providers.last_used_at` (timestamptz), `ads_insights.reach`
(bigint), e a constraint `ai_providers_provider_check` liberando `gemini`,
`openai`, `openrouter`, `anthropic`. Nenhuma ação adicional necessária
aqui — Fases A e B já funcionam em produção com o schema correto.

## O que NÃO foi verificado nesta rodada (peço atenção)
- **"Sign in with ChatGPT" (SIWC) para usar o plano ChatGPT Plus de cada
  cliente dentro do app:** pesquisei a documentação oficial atual
  (developers.openai.com/siwc e os termos de uso). Existe de fato uma
  modalidade chamada "ChatGPT plan usage", mas os termos (vigentes desde
  04/11/2026) exigem: (1) aprovação prévia da OpenAI via formulário de
  interesse para apps pagos/hospedados remotamente, (2) os tokens de
  autenticação ficarem **só no dispositivo do usuário** ("not in a remote or
  managed environment"), e (3) as chamadas saírem do runtime local do
  próprio usuário. Como o backend hoje roda centralizado na Vercel (chat
  processado no servidor, não no dispositivo do cliente), **a arquitetura
  atual não se encaixa nessa modalidade mesmo que a OpenAI aprovasse** —
  encaixaria uma CLI/app 100% local, não este SaaS hospedado. Recomendação:
  manter como está (chave de API paga do próprio OpenAI, já suportada no
  hub) e tratar SIWC como possível upside futuro, não como algo a implementar
  agora.
- **Modelo BYOK "pague uma vez, cada cliente usa sua própria chave" (Etapa 3):**
  encontrei uma inconsistência que precisa de uma decisão sua antes de eu
  mexer em código. O hub de IA por usuário (`/api/providers`, Fase A) já
  suporta OpenAI/Gemini/OpenRouter/Anthropic com chave própria por cliente —
  mas ele alimenta só algumas funcionalidades (ex.: `/api/providers/generate`).
  **O motor principal do Chat (`/api/chat`, usado por Gestor/Mentor, Criar
  Anúncio, Auditoria etc.) continua lendo chaves de variáveis de ambiente do
  SERVIDOR** (`NVIDIA_API_KEY`, `OPENAI_API_KEY` etc. em `_build_registry()`),
  **compartilhadas entre todos os clientes**, não por comprador. NVIDIA NIM
  em particular não está no hub por usuário. Antes de eu alterar isso
  (mudança de arquitetura real, não cosmética), preciso que você confirme:
  o Chat principal também deve passar a usar a chave do próprio cliente, ou
  o modelo comercial aceita que o Chat use uma chave sua (do servidor) e só
  os recursos avançados sejam BYOK?
- **Isolamento entre compradores:** é lógico (linhas filtradas por `email`/
  `owner_email` em todas as tabelas do Supabase), não é um banco de dados
  separado por cliente. Todos os compradores de hoje compartilham: o mesmo
  projeto Supabase, o mesmo app Meta (`META_APP_ID`/`META_APP_SECRET`
  registrado nos seus Apps do Facebook) e o mesmo backend na Vercel. Isso é
  normal para um SaaS, mas é importante você saber antes de vender como
  "instalável" — o instalador (PWA/Tauri) é uma casca de acesso a esse
  mesmo serviço compartilhado, não uma cópia isolada por cliente.

## O que roda local vs. o que depende de internet (Etapa 5)

O app **não tem modo totalmente offline**. Tabela do que cada peça depende:

| Peça | Local (sem internet)? | Depende de |
|---|---|---|
| Janela do app Tauri abrir | Sim (é só a casca do webview) | — |
| Qualquer tela com dados (Chat, Painel, Rastreamento, Financeiro, Campanha) | Não | Vercel (backend) |
| Login / conta do comprador | Não | Supabase (`app_users`, `app_buyers`) |
| Conectar Meta Ads, ver campanhas, criar campanha | Não | Vercel + Meta Graph API + Supabase |
| Central de IA (qualquer provedor) | Não | Vercel + o provedor de IA escolhido |
| PWA instalado | Mesma coisa — é o mesmo site, só com atalho/janela própria | Vercel |
| Service worker (`sw.js`) | Parcial — só reexibe a última tela carregada se a internet cair, não funciona "de verdade" offline | — |

## Instruções para execução local (desenvolvimento)

```bash
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env   # preencha ao menos uma chave de IA (NVIDIA_API_KEY é gratuita)
uvicorn app_core:create_app --factory --reload
# abre http://localhost:8000
```

Testes: `python -m pytest -q` (não precisa de Supabase nem de chaves reais —
tudo mockado, exceto `test_api.py`/`test_athena_integration.py`, que o
`pytest.ini` já ignora por serem scripts manuais).

## Arquivos responsáveis pela interface

- `static/index.html` — **toda** a UI (SPA de arquivo único, ~1500+ linhas de
  JS inline). Seções principais por `id` de `<section class="sec">`:
  `chatSection`/home, `adsSection` (Painel de anúncios), `trackingSection`
  (Rastreamento), `financeSection` (Financeiro), `campwizSection` (Publicar
  Campanha), `provSection` (Central de IA), `claudeSection` (Conectar ao
  Claude), `bibSection` (Biblioteca).
- `configs/meta-ads*.json` (6 idiomas) — todo o texto, prompts e o grid de
  ferramentas do Chat (`tools`/`prompts`/`v2menu`). **Editar um sem editar
  os outros 5 quebra a paridade entre idiomas** — use um script Python para
  manter os 6 em sincronia (padrão usado em todas as fases desta
  consolidação).
- `app_core.py` — backend genérico do App Factory (chat, branding, central
  de IA, PWA).
- `ads_connect.py` — tudo de Meta Ads (OAuth, insights, criação de
  campanha/conjunto, ferramentas MCP).
- `finance.py` — calculadora de break-even (puro, sem dependências).
- `src-tauri/` — casca desktop (não tem UI própria, só aponta pra URL de
  produção em `tauri.conf.json`).

## Instruções para gerar os instaladores

Ver `docs/app-instalavel.md` (seção "Gerando os instaladores você mesmo") —
requer Rust + `cargo install tauri-cli`. Em CI, `.github/workflows/
desktop-release.yml` faz isso automaticamente a cada tag `v*` ou execução
manual ("Run workflow").

## Próximo passo

Redesign visual pelo Codex, com a logo oficial e referências de interface
fornecidas separadamente. Nenhum módulo novo deve ser adicionado fora desse
escopo nesta próxima etapa.

Depois do redesign, ver `modelo-produto-local-servidor.md` (mesma pasta) para
o plano do Modo Local e Modo Servidor 24h do produto — ainda não implementado,
só planejado, para não atrasar esta entrega.
