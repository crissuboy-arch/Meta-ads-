"""Central de IA (hub de provedores) — testes unitarios, tudo mockado.

Nao depende de Supabase nem de chaves reais; roda em qualquer maquina/CI.
"""
import json

import pytest

import app_core


class _Resp:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status
        self.content = json.dumps(payload).encode()

    def json(self):
        return self._payload


def test_prov_text_anthropic_calls_messages_api(monkeypatch):
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return _Resp({"content": [{"type": "text", "text": "ok, funcionando"}]})

    monkeypatch.setattr(app_core._requests, "post", fake_post)

    out = app_core._prov_text("anthropic", "sk-ant-test", "claude-sonnet-4-5", "diga ok")

    assert out == "ok, funcionando"
    assert captured["url"] == "https://api.anthropic.com/v1/messages"
    assert captured["headers"]["x-api-key"] == "sk-ant-test"
    assert captured["headers"]["anthropic-version"] == "2023-06-01"
    assert captured["json"]["model"] == "claude-sonnet-4-5"
    assert captured["json"]["messages"] == [{"role": "user", "content": "diga ok"}]


def test_prov_text_anthropic_empty_response_raises(monkeypatch):
    monkeypatch.setattr(
        app_core._requests, "post",
        lambda *a, **k: _Resp({"content": [{"type": "text", "text": "  "}]}))

    with pytest.raises(RuntimeError, match="empty_response"):
        app_core._prov_text("anthropic", "sk-ant-test", "claude-sonnet-4-5", "diga ok")


def test_prov_text_anthropic_http_error_raises(monkeypatch):
    monkeypatch.setattr(
        app_core._requests, "post",
        lambda *a, **k: _Resp({"error": {"message": "invalid key"}}, status=401))

    with pytest.raises(RuntimeError, match="provider_http_401"):
        app_core._prov_text("anthropic", "bad-key", "claude-sonnet-4-5", "diga ok")


def test_prov_default_models_has_anthropic_text():
    assert app_core._PROV_DEFAULT_MODELS[("anthropic", "text")] == "claude-sonnet-4-5"
