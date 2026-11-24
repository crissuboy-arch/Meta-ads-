"""Fase D: calculadora financeira (break-even) - funcoes puras + endpoint
/api/finance/calc de ponta a ponta. Sem Supabase, sem chave de IA.
"""
import os

import pytest
from fastapi.testclient import TestClient

import finance


def test_calc_breakeven_basic():
    out = finance.calc_breakeven(
        price=100.0, gateway_fee_pct=10.0, gateway_fee_fixed=2.0,
        other_costs=8.0, target_margin_pct=20.0)
    # net = 100 - 10 (10%) - 2 (fixa) - 8 (outros) = 80
    assert out["net_price_per_sale"] == 80.0
    # max_cpa = 80 - (100*0.20) = 60
    assert out["max_cpa"] == 60.0
    # breakeven_roas = 100 / 80 = 1.25
    assert out["breakeven_roas"] == 1.25
    assert out["net_profit"] is None


def test_calc_breakeven_with_period_data():
    out = finance.calc_breakeven(price=50.0, gateway_fee_pct=0, other_costs=10.0,
                                  ad_spend=300.0, purchases=20)
    # net = 50 - 10 = 40; net_profit = 20*40 - 300 = 500
    assert out["net_price_per_sale"] == 40.0
    assert out["net_profit"] == 500.0


def test_calc_breakeven_unprofitable_net_price_no_roas_division_by_zero():
    out = finance.calc_breakeven(price=20.0, other_costs=25.0)
    assert out["net_price_per_sale"] == -5.0
    assert out["breakeven_roas"] is None  # nao divide por zero/negativo


def test_calc_breakeven_invalid_price_raises():
    with pytest.raises(ValueError):
        finance.calc_breakeven(price=0)
    with pytest.raises(ValueError):
        finance.calc_breakeven(price=-10)


def _build_app():
    os.environ.setdefault("NVIDIA_API_KEY", "dummy-test-key")
    import app_core
    return app_core.create_app()


def test_endpoint_calc_breakeven():
    client = TestClient(_build_app())
    r = client.post("/api/finance/calc", json={
        "price": 100, "gateway_fee_pct": 10, "gateway_fee_fixed": 2,
        "other_costs": 8, "target_margin_pct": 20,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["net_price_per_sale"] == 80.0
    assert body["max_cpa"] == 60.0


def test_endpoint_rejects_missing_price():
    client = TestClient(_build_app())
    r = client.post("/api/finance/calc", json={})
    assert r.status_code == 400


def test_endpoint_rejects_zero_price():
    client = TestClient(_build_app())
    r = client.post("/api/finance/calc", json={"price": 0})
    assert r.status_code == 400
