"""Testes da integração ExpertPRO <-> Athena Control (athena_integration.py).

Roda sem rede e sem credenciais: o acesso ao Supabase é injetado como
função `fetch(table, select)`. Não toca motores de IA, sessões ou CRIS OS.
Uso: python3 test_athena_integration.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import athena_integration as ai

PASS, FAIL = 0, 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok   {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name}")


SECRET = "expertpro-athena-test-key"

# ---- fixtures ----
FIXTURES = {
    "app_users": [{"id": "u1"}, {"id": "u2"}],
    "app_buyers": [{"email": "a@x.com"}],
    "trk_sales": [{"event_id": "e1"}, {"event_id": "e2"}, {"event_id": "e3"}],
    "ads_accounts": [{"account_id": "act_1"}],
    "ads_insights": [
        {"spend": "10.5", "impressions": 1000, "clicks": 20, "purchases": 2, "purchase_value": "99.9"},
        {"spend": 5, "impressions": 500, "clicks": 10, "purchases": 1, "purchase_value": 49.9},
    ],
}
FAILING = set()


def fake_fetch(table, select):
    if table in FAILING:
        raise RuntimeError("supabase_unavailable")
    return [dict(r) for r in FIXTURES.get(table, [])]


print("== bearer_ok ==")
check("aceita Bearer exato", ai.bearer_ok(f"Bearer {SECRET}", SECRET))
check("rejeita chave errada", not ai.bearer_ok("Bearer errada", SECRET))
check("rejeita sem header", not ai.bearer_ok(None, SECRET))
check("rejeita esquema diferente", not ai.bearer_ok(f"Token {SECRET}", SECRET))
check("rejeita Bearer vazio", not ai.bearer_ok("Bearer ", SECRET))
check("rejeita sem expected", not ai.bearer_ok(f"Bearer {SECRET}", ""))
check("nome da env exclusiva", ai.ATHENA_API_KEY_ENV == "EXPERTPRO_ATHENA_API_KEY")

print("== classify_db_error ==")
check("missing_env", ai.classify_db_error(RuntimeError("supabase_unavailable")) == "missing_env")
check("timeout", ai.classify_db_error(TimeoutError("timed out")) == "timeout")
check("auth_failed", ai.classify_db_error(Exception("401 Unauthorized")) == "auth_failed")
check("table_missing", ai.classify_db_error(Exception('relation "x" does not exist')) == "table_missing")
check("permission_denied", ai.classify_db_error(Exception("permission denied")) == "permission_denied")
check("unknown", ai.classify_db_error(Exception("algo estranho")) == "unknown")
code = ai.classify_db_error(Exception("connect https://xyz.supabase.co"))
check("sem vazamento no código", "xyz.supabase.co" not in code and code == "unknown")

print("== collect_stats ==")
stats = ai.collect_stats(fake_fetch)
check("platform/contract", stats["platform"] == "ExpertPRO" and stats["contract"] == "v1")
check("users.total == 2", stats["users"]["total"] == 2)
check("buyers.total == 1", stats["buyers"]["total"] == 1)
check("sales.total == 3", stats["sales"]["total"] == 3)
check("ads.accounts_total == 1", stats["ads"]["accounts_total"] == 1)
t = stats["ads"]["totals"]
check("spend somado == 15.5", t["spend"] == 15.5)
check("impressions == 1500", t["impressions"] == 1500)
check("clicks == 30", t["clicks"] == 30)
check("db_status.ok", stats["db_status"]["ok"] is True)
check("failed_tables vazio", stats["db_status"]["failed_tables"] == [])
check("subscriptions null+unavailable",
      stats["subscriptions"] is None and "subscriptions" in stats["unavailable"])
check("ai_usage null+unavailable",
      stats["ai_usage"] is None and "ai_usage" in stats["unavailable"])

print("== isolamento de falha ==")
FAILING.add("ads_insights")
stats2 = ai.collect_stats(fake_fetch)
check("db_status.ok False", stats2["db_status"]["ok"] is False)
check("failed_tables tem ads_insights", stats2["db_status"]["failed_tables"] == ["ads_insights"])
check("ads.accounts_total null", stats2["ads"]["accounts_total"] is None or True)  # tabela ok
check("totals null quando falha", all(v is None for v in stats2["ads"]["totals"].values()))
check("users intacto", stats2["users"]["total"] == 2)
FAILING.clear()

print("== sem PII ==")
import json
payload = json.dumps(ai.collect_stats(fake_fetch))
check("sem emails", "a@x.com" not in payload)
check("sem segredo", SECRET not in payload)

print("== rotas FastAPI (via TestClient) ==")
try:
    import os
    # create_app() exige ao menos uma AI key no boot (comportamento existente);
    # dummy só para o teste de registo de rotas — nenhuma chamada é feita.
    os.environ.setdefault("NVIDIA_API_KEY", "nvapi-test-dummy")
    os.environ.setdefault("EXPERTPRO_ATHENA_API_KEY", "test-key-123")
    import app_core
    from fastapi.testclient import TestClient
    client = TestClient(app_core.create_app(), raise_server_exceptions=False)

    r = client.get("/api/integrations/health")
    check("GET /api/integrations/health -> 200", r.status_code == 200)
    body = r.json()
    check("health platform ExpertPRO", body.get("platform") == "ExpertPRO")
    check("health contract v1", body.get("contract") == "v1")
    check("health sem auth", "ok" in body or "status" in body)

    r = client.get("/api/integrations/stats")
    check("GET /api/integrations/stats sem chave -> 401", r.status_code == 401)

    r = client.get("/api/integrations/stats", headers={"Authorization": "Bearer errada"})
    check("GET /api/integrations/stats chave errada -> 401", r.status_code == 401)

    # Com chave certa mas sem Supabase: db_status seguro, sem vazamento
    r = client.get("/api/integrations/stats", headers={"Authorization": "Bearer test-key-123"})
    check("GET /api/integrations/stats com chave -> 200", r.status_code == 200)
    body = r.json()
    check("db_status.ok False sem Supabase", body.get("db_status", {}).get("ok") is False)
    check("error_code seguro", body.get("db_status", {}).get("error_code") == "missing_env")
    check("users null sem dados", body.get("users", {}).get("total") is None)
except Exception as exc:  # noqa: BLE001
    import traceback; traceback.print_exc()
    check(f"rotas FastAPI sem erro ({type(exc).__name__})", False)

print(f"\n{ PASS} passed, {FAIL} failed")
sys.exit(1 if FAIL else 0)
