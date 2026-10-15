# ExpertPRO ↔ Athena Control — integração somente-leitura

Segue o padrão validado nas integrações VitrinePro, Pink Logic e ScalaFlow.

## Endpoints

| Método | Rota | Auth |
|---|---|---|
| GET | `/api/integrations/health` | pública |
| GET | `/api/integrations/stats` | `Authorization: Bearer <EXPERTPRO_ATHENA_API_KEY>` |

Sem chave → **401**. Com chave errada → **401**. Sem `EXPERTPRO_ATHENA_API_KEY`
configurada no servidor → **503** (não é falha de auth).

## Indicadores reais (somente leitura, zero PII)

- `users.total` — contagem de `app_users`
- `buyers.total` — contagem de `app_buyers`
- `sales.total` — contagem de eventos em `trk_sales`
- `ads.accounts_total` — contagem de `ads_accounts`
- `ads.totals` — somas reais de `ads_insights`: `spend`, `impressions`,
  `clicks`, `purchases`, `purchase_value`
- `db_status` — `{ok, error_code, failed_tables}`; códigos seguros
  (`missing_env`, `timeout`, `dns_error`, `connection_error`, `auth_failed`,
  `permission_denied`, `table_missing`, `unknown`) — nunca URLs ou chaves
- `subscriptions` / `ai_usage` — sempre `null`, listados em `unavailable`
  (não existem tabelas para isso no Supabase do projeto)

Falha numa tabela não derruba as outras: o indicador afetado vira `null`,
`db_status.ok=false` e `failed_tables` diz qual tabela falhou.

## Chave exclusiva

Variável de ambiente no servidor (Vercel → Project Settings → Environment
Variables, ou `.env` local):

```
EXPERTPRO_ATHENA_API_KEY=<valor-da-chave>
```

- Nunca vai para o git, chat ou logs.
- É exclusiva desta integração (não partilhada com outras plataformas).

## Cadastro no Athena Connect

- **Plataforma:** `ExpertPRO`
- **Tipo:** `API`
- **URL:** `https://<seu-dominio>/api/integrations/stats`
- Guardar `EXPERTPRO_ATHENA_API_KEY` no cofre da Athena e clicar **Verificar**.

## Testes

```bash
python3 test_athena_integration.py   # 43 testes, sem rede, sem credenciais
```

## Ficheiros

- `athena_integration.py` — lógica pura (Bearer timing-safe, classificação
  de erros, agregados em paralelo). Não toca motores de IA, automações,
  webhooks, MCP, sessões ou CRIS OS.
- `app_core.py` — regista as 2 rotas dentro de `create_app()`; `/stats`
  usa o `_sb_req` já existente (REST Supabase com `SUPABASE_URL` +
  `SUPABASE_SERVICE_KEY`).

## Limites honestos

- Sem Supabase configurado, todos os indicadores vêm `null` com
  `db_status.error_code="missing_env"` — o `null` não é dado válido.
- Os totais de `ads_insights` refletem o que está guardado no banco;
  nenhuma campanha, receita ou métrica é inventada.
