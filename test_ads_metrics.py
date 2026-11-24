"""Metricas derivadas do Meta Ads (CPA/CPC/CPM/frequencia) — tudo mockado.

Nao depende de Supabase nem de token real da Meta; roda em qualquer maquina/CI.
"""
from fastapi import FastAPI
from fastapi.testclient import TestClient

import ads_connect

_ROWS = [
    {"account_id": "1", "day": "2026-11-20", "campaign_id": "c1", "campaign_name": "Oferta A",
     "spend": 100.0, "impressions": 10000, "reach": 5000, "clicks": 200,
     "purchases": 10, "purchase_value": 500.0},
    {"account_id": "1", "day": "2026-11-21", "campaign_id": "c1", "campaign_name": "Oferta A",
     "spend": 50.0, "impressions": 5000, "reach": 2500, "clicks": 100,
     "purchases": 0, "purchase_value": 0.0},
]


def _build_app(rows):
    app = FastAPI()

    @app.middleware("http")
    async def _fake_auth(request, call_next):
        request.state.user_email = "test@example.com"
        return await call_next(request)

    def fake_sb_req(method, table, params=None, payload=None):
        if method == "GET" and table == "ads_insights":
            return rows
        return []

    d = {
        "sb_req": fake_sb_req,
        "sb_target": lambda: ("https://example.supabase.co", "service-key"),
        "auth_secret": lambda: b"test-secret",
        "scrub": lambda s: s,
        "requests": None,
        "b64u": lambda b: "",
        "b64u_dec": lambda s: b"",
        "mcp": {},
    }
    ads_connect.register(app, d)
    return app


def test_insights_totals_include_derived_metrics():
    client = TestClient(_build_app(_ROWS))
    r = client.get("/api/ads/insights?days=30")
    assert r.status_code == 200
    tot = r.json()["totals"]

    assert tot["spend"] == 150.0
    assert tot["impressions"] == 15000
    assert tot["reach"] == 7500
    assert tot["clicks"] == 300
    assert tot["purchases"] == 10
    # cpa = spend / purchases
    assert tot["cpa"] == 15.0
    # cpc = spend / clicks
    assert tot["cpc"] == 0.5
    # cpm = spend / impressions * 1000
    assert tot["cpm"] == 10.0
    # frequency = impressions / reach
    assert tot["frequency"] == 2.0


def test_insights_campaign_has_derived_metrics():
    client = TestClient(_build_app(_ROWS))
    r = client.get("/api/ads/insights?days=30")
    camp = r.json()["campaigns"][0]
    assert camp["campaign_id"] == "c1"
    assert camp["cpa"] == 15.0
    assert camp["cpc"] == 0.5
    assert camp["cpm"] == 10.0
    assert camp["frequency"] == 2.0


def test_insights_zero_purchases_and_reach_gives_none_not_crash():
    rows = [{"account_id": "1", "day": "2026-11-21", "campaign_id": "c2", "campaign_name": "Sem venda",
             "spend": 20.0, "impressions": 100, "reach": 0, "clicks": 0,
             "purchases": 0, "purchase_value": 0.0}]
    client = TestClient(_build_app(rows))
    r = client.get("/api/ads/insights?days=30")
    camp = r.json()["campaigns"][0]
    assert camp["cpa"] is None
    assert camp["cpc"] is None
    assert camp["frequency"] is None
    assert camp["cpm"] == 200.0
