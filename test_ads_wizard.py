"""Fase E: assistente de campanha pela web (/api/ads/wizard/*) - tudo
mockado (Supabase e Meta Graph API). Reaproveita os mesmos handlers do
MCP (t_create_campaign etc.), nao duplica logica nenhuma.
"""
import base64
import hashlib
import hmac
import json
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


class _Resp:
    def __init__(self, payload, status=200):
        self._p, self.status_code = payload, status
        self.text = json.dumps(payload)

    def json(self):
        return self._p


def _build_app(requests_fake, monkeypatch, write_enabled=False):
    if write_enabled:
        monkeypatch.setenv("WRITE_ACTIONS_ENABLED", "true")
    else:
        monkeypatch.delenv("WRITE_ACTIONS_ENABLED", raising=False)

    app = FastAPI()

    @app.middleware("http")
    async def _fake_auth(request, call_next):
        request.state.user_email = "test@example.com"
        return await call_next(request)

    token_enc = _enc_token("real-meta-token")

    def fake_sb_req(method, table, params=None, payload=None):
        if table == "ads_connections" and method == "GET":
            return [{"token_enc": token_enc}]
        if table == "ads_accounts" and method == "GET":
            return [{"account_id": "999", "name": "Conta Teste", "currency": "BRL"}]
        return []

    d = {
        "sb_req": fake_sb_req,
        "sb_target": lambda: ("https://example.supabase.co", "service-key"),
        "auth_secret": lambda: AUTH_SECRET,
        "scrub": lambda s: s,
        "requests": requests_fake,
        "b64u": _b64u,
        "b64u_dec": _b64u_dec,
        "mcp": {},
    }
    ads_connect.register(app, d)
    return app


class _FakeRequests:
    """Mock minimo de requests.get/post para a Graph API."""
    def __init__(self, response):
        self.response = response
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append(("GET", url, params))
        return self.response

    def post(self, url, params=None, data=None, timeout=None):
        self.calls.append(("POST", url, params, data))
        return self.response


def test_wizard_meta_lists_objectives_and_flag_state(monkeypatch):
    app = _build_app(_FakeRequests(_Resp({})), monkeypatch, write_enabled=False)
    client = TestClient(app)
    r = client.get("/api/ads/wizard/meta")
    assert r.status_code == 200
    body = r.json()
    assert "OUTCOME_SALES" in body["objectives"]
    assert body["write_actions_enabled"] is False


def test_wizard_blocks_create_campaign_when_write_disabled(monkeypatch):
    app = _build_app(_FakeRequests(_Resp({"id": "123"})), monkeypatch, write_enabled=False)
    client = TestClient(app)
    r = client.post("/api/ads/wizard/call", json={
        "tool": "create_campaign",
        "human_confirmed": True,
        "args": {"ad_account_id": "999", "name": "Teste", "objective": "OUTCOME_SALES"},
    })
    assert r.status_code == 403


def test_wizard_allows_read_tool_even_when_write_disabled(monkeypatch):
    fake = _FakeRequests(_Resp({"data": [{"id": "1", "name": "Campanha X"}]}))
    app = _build_app(fake, monkeypatch, write_enabled=False)
    client = TestClient(app)
    r = client.post("/api/ads/wizard/call", json={
        "tool": "list_objects", "args": {"ad_account_id": "999", "level": "campaigns"},
    })
    assert r.status_code == 200
    assert r.json()["items"][0]["name"] == "Campanha X"


def test_wizard_creates_paused_campaign_when_write_enabled(monkeypatch):
    fake = _FakeRequests(_Resp({"id": "777888999"}))
    app = _build_app(fake, monkeypatch, write_enabled=True)
    client = TestClient(app)
    r = client.post("/api/ads/wizard/call", json={
        "tool": "create_campaign",
        "args": {"ad_account_id": "999", "name": "Oferta nova", "objective": "OUTCOME_SALES"},
        "human_confirmed": True,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["campaign_id"] == "777888999"
    assert body["status"] == "PAUSED"
    # confirma que o payload enviado ao Meta pedia status=PAUSED
    method, url, params, data = fake.calls[-1]
    assert data["status"] == "PAUSED"


def test_wizard_rejects_activate_without_explicit_confirmation(monkeypatch):
    fake = _FakeRequests(_Resp({"success": True}))
    app = _build_app(fake, monkeypatch, write_enabled=True)
    client = TestClient(app)
    r = client.post("/api/ads/wizard/call", json={
        "tool": "set_status", "args": {"object_id": "123", "status": "ACTIVE"},
    })
    assert r.status_code == 403
    assert "human_approval_required" in r.json()["detail"]
