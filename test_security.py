"""Fase F: seguranca e controle.

1) Teto de orcamento diario (MAX_DAILY_BUDGET_CENTS) via to_minor(), o
   unico ponto por onde create_campaign/create_adset convertem orcamento.
2) Prova de que chaves/tokens nunca saem inteiros do servidor: /api/providers
   e a listagem de contas Meta so devolvem metadados (has_key/hint), nunca
   o segredo em si.
"""
import base64
import hashlib
import hmac
import os
import secrets

from fastapi import FastAPI
from fastapi.testclient import TestClient

import ads_connect

AUTH_SECRET = b"test-secret-32-bytes-xxxxxxxxxxx"


def _b64u(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _b64u_dec(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def _enc_token(text: str) -> str:
    """Replica ads_connect.enc() para preparar um token_enc valido nos testes."""
    base = hashlib.sha256(b"ads-token|" + AUTH_SECRET).digest()
    ek = hmac.new(base, b"enc", hashlib.sha256).digest()
    mk = hmac.new(base, b"mac", hashlib.sha256).digest()
    nonce = secrets.token_bytes(16)
    raw = text.encode()
    stream, i = b"", 0
    while len(stream) < len(raw):
        stream += hmac.new(ek, nonce + i.to_bytes(4, "big"), hashlib.sha256).digest()
        i += 1
    ct = bytes(a ^ b for a, b in zip(raw, stream))
    tag = hmac.new(mk, nonce + ct, hashlib.sha256).digest()
    return _b64u(nonce + ct + tag)


_TOKEN_ENC = _enc_token("real-meta-token-never-leak-me")


def _register(fake_sb_req):
    """Registra ads_connect numa app isolada e devolve o dispatcher mcp_call."""
    app = FastAPI()
    d = {
        "sb_req": fake_sb_req,
        "sb_target": lambda: ("https://example.supabase.co", "service-key"),
        "auth_secret": lambda: AUTH_SECRET,
        "scrub": lambda s: s,
        "requests": None,
        "b64u": _b64u,
        "b64u_dec": _b64u_dec,
        "mcp": {},
    }
    ads_connect.register(app, d)
    return d["mcp"]["call"]


def _fake_sb_req(method, table, params=None, payload=None):
    if table == "ads_accounts" and method == "GET":
        return [{"account_id": "999", "name": "Conta Teste", "currency": "BRL",
                  "status": "ACTIVE", "selected": True}]
    if table == "ads_connections" and method == "GET":
        # token_enc: a forma real como o token fica guardado (criptografado).
        # Nunca deveria aparecer inteiro ("real-meta-token-never-leak-me")
        # em nenhuma resposta da API.
        return [{"token_enc": _TOKEN_ENC}]
    return []


def test_budget_cap_blocks_expensive_campaign(monkeypatch):
    monkeypatch.setenv("MAX_DAILY_BUDGET_CENTS", "5000")  # R$50,00/dia
    mcp_call = _register(_fake_sb_req)
    out = mcp_call("test@example.com", "create_campaign",
                    {"ad_account_id": "999", "name": "Oferta cara",
                     "objective": "OUTCOME_SALES", "daily_budget": 200})
    assert out["isError"] is True
    assert "MAX_DAILY_BUDGET_CENTS" in out["content"][0]["text"]


def test_budget_within_cap_is_not_rejected_by_cap(monkeypatch):
    monkeypatch.setenv("MAX_DAILY_BUDGET_CENTS", "5000")
    mcp_call = _register(_fake_sb_req)
    out = mcp_call("test@example.com", "create_campaign",
                    {"ad_account_id": "999", "name": "Oferta ok",
                     "objective": "OUTCOME_SALES", "daily_budget": 10})
    # Sem "requests" real a chamada à Graph API falha adiante - o que importa
    # aqui é que o teto NÃO seja o motivo da rejeição.
    if out.get("isError"):
        assert "MAX_DAILY_BUDGET_CENTS" not in out["content"][0]["text"]


def test_no_cap_set_does_not_block_anything(monkeypatch):
    monkeypatch.delenv("MAX_DAILY_BUDGET_CENTS", raising=False)
    mcp_call = _register(_fake_sb_req)
    out = mcp_call("test@example.com", "create_campaign",
                    {"ad_account_id": "999", "name": "Sem teto",
                     "objective": "OUTCOME_SALES", "daily_budget": 100000})
    if out.get("isError"):
        assert "MAX_DAILY_BUDGET_CENTS" not in out["content"][0]["text"]


def test_providers_endpoint_never_leaks_full_key(monkeypatch):
    os.environ.setdefault("NVIDIA_API_KEY", "dummy-test-key")
    import app_core

    def fake_sb_req(method, table, params=None, payload=None):
        if table == "ai_providers" and method == "GET":
            return [{"id": "u|text|primary", "provider": "openai", "kind": "text",
                      "role": "primary", "model": "gpt-4o-mini",
                      "key_enc": "ENCRYPTED-BLOB-NEVER-EXPOSE", "key_hint": "…abcd",
                      "active": True, "last_test_ok": True}]
        return []

    monkeypatch.setattr(app_core, "_sb_req", fake_sb_req, raising=False)
    app = app_core.create_app()
    client = TestClient(app)
    r = client.get("/api/providers")
    assert "ENCRYPTED-BLOB-NEVER-EXPOSE" not in r.text


def test_list_ad_accounts_never_returns_token():
    mcp_call = _register(_fake_sb_req)
    out = mcp_call("test@example.com", "list_ad_accounts", {})
    text = out["content"][0]["text"]
    assert "real-meta-token-never-leak-me" not in text
    assert "token" not in text.lower()
