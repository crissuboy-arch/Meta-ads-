"""Integração somente-leitura ExpertPRO <-> Athena Control.

Segue o padrão validado nas integrações VitrinePro, Pink Logic e ScalaFlow:
  GET /api/integrations/health  (público)
  GET /api/integrations/stats   (Authorization: Bearer EXPERTPRO_ATHENA_API_KEY)

Somente agregados reais das tabelas que já existem no Supabase
(app_users, app_buyers, trk_sales, ads_accounts, ads_insights).
Zero PII: só contagens e somas. Linhas individuais nunca saem daqui.

Este módulo nunca toca motores de IA, automações, webhooks, MCP,
sessões ou CRIS OS — é leitura de agregados, nada mais.
"""

import hashlib
import hmac
from concurrent.futures import ThreadPoolExecutor, as_completed

ATHENA_PLATFORM = "ExpertPRO"
ATHENA_CONTRACT = "v1"
ATHENA_API_KEY_ENV = "EXPERTPRO_ATHENA_API_KEY"

# Teto total do lote de consultas (cada consulta do _sb_req já tem
# timeout próprio de 15s; o agregado nunca deve travar o endpoint).
STATS_TIMEOUT_S = 25


def bearer_ok(auth_header, expected):
    """Timing-safe Bearer compare contra a chave exclusiva do ExpertPRO."""
    if not expected or not (auth_header or "").startswith("Bearer "):
        return False
    provided = auth_header[len("Bearer "):].strip()
    if not provided:
        return False
    a = hashlib.sha256(provided.encode()).digest()
    b = hashlib.sha256(expected.encode()).digest()
    return len(a) == len(b) and hmac.compare_digest(a, b)


def classify_db_error(exc):
    """Mapeia exceções para códigos seguros (sem URLs, chaves ou mensagens)."""
    name = type(exc).__name__
    msg = str(exc or "")
    if "supabase_unavailable" in msg or name == "RuntimeError" and "supabase" in msg.lower():
        return "missing_env"
    if name in ("ConnectTimeout", "ReadTimeout", "Timeout") or "timeout" in name.lower():
        return "timeout"
    if "timeout" in msg.lower() or "timed out" in msg.lower():
        return "timeout"
    # requests.ConnectionError: distingue DNS de conexão recusada pelo texto
    if "ConnectionError" in name or "Failed to establish" in msg or "Max retries" in msg:
        low = msg.lower()
        if "nameresolution" in low or "nodename nor servname" in low or "getaddrinfo failed" in low:
            return "dns_error"
        if "refused" in low:
            return "connection_error"
        return "connection_error"
    if "401" in msg or "Unauthorized" in msg or "Invalid API key" in msg:
        return "auth_failed"
    if "403" in msg or "permission denied" in msg.lower():
        return "permission_denied"
    if "42P01" in msg or "does not exist" in msg:
        return "table_missing"
    return "unknown"


def _safe_float(v):
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def _fetch_counts(fetch):
    """Roda as 5 consultas em paralelo. Retorna dict chave -> (valor, error_code)."""
    specs = {
        "users": ("app_users", "id"),
        "buyers": ("app_buyers", "email"),
        "sales": ("trk_sales", "event_id"),
        "ads_accounts": ("ads_accounts", "account_id"),
        "ads_insights": ("ads_insights", "spend,impressions,clicks,purchases,purchase_value"),
    }

    def one(key):
        table, select = specs[key]
        try:
            rows = fetch(table, select) or []
            return key, rows, None
        except Exception as exc:  # noqa: BLE001 - isolado por tabela
            return key, None, classify_db_error(exc)

    results = {}
    with ThreadPoolExecutor(max_workers=5) as pool:
        futs = {pool.submit(one, k): k for k in specs}
        for fut in as_completed(futs, timeout=STATS_TIMEOUT_S):
            key, rows, err = fut.result()
            results[key] = (rows, err)
    # Garante todas as chaves mesmo se o timeout global estourar
    for key in specs:
        results.setdefault(key, (None, "timeout"))
    return results


def collect_stats(fetch):
    """Agregados reais. `fetch(table, select)` -> lista de dicts (levanta se falhar)."""
    results = _fetch_counts(fetch)

    def count(key):
        rows, _ = results[key]
        return len(rows) if rows is not None else None

    def failed(key):
        _, err = results[key]
        return err

    insights_rows, _ = results["ads_insights"]
    if insights_rows is None:
        ads_totals = {k: None for k in ("spend", "impressions", "clicks", "purchases", "purchase_value")}
    else:
        ads_totals = {
            "spend": round(sum(_safe_float(r.get("spend")) for r in insights_rows), 2),
            "impressions": int(sum(_safe_float(r.get("impressions")) for r in insights_rows)),
            "clicks": int(sum(_safe_float(r.get("clicks")) for r in insights_rows)),
            "purchases": round(sum(_safe_float(r.get("purchases")) for r in insights_rows), 2),
            "purchase_value": round(sum(_safe_float(r.get("purchase_value")) for r in insights_rows), 2),
        }

    table_of = {
        "users": "app_users",
        "buyers": "app_buyers",
        "sales": "trk_sales",
        "ads_accounts": "ads_accounts",
        "ads_insights": "ads_insights",
    }
    failed_tables = []
    codes = []
    for key, table in table_of.items():
        err = failed(key)
        if err:
            failed_tables.append(table)
            codes.append(err)

    return {
        "platform": ATHENA_PLATFORM,
        "contract": ATHENA_CONTRACT,
        "users": {"total": count("users")},
        "buyers": {"total": count("buyers")},
        "sales": {"total": count("sales")},
        "ads": {
            "accounts_total": count("ads_accounts"),
            "totals": ads_totals,
        },
        "db_status": {
            "ok": not failed_tables,
            "error_code": codes[0] if codes else None,
            "failed_tables": failed_tables,
        },
        "subscriptions": None,
        "ai_usage": None,
        "unavailable": ["subscriptions", "ai_usage"],
        "notes": {
            "users": "Contagem de app_users (sem PII).",
            "buyers": "Contagem de app_buyers (sem PII).",
            "sales": "Contagem de eventos em trk_sales.",
            "ads": "Agregados de ads_insights (somas reais do banco).",
            "db_status": "ok=false significa falha no banco — os nulls não são dados válidos.",
            "subscriptions": "Não existe tabela de assinaturas — indisponível.",
            "ai_usage": "Não existe tabela de uso de IA — indisponível.",
        },
    }
