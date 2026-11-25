"""Fase G (parte 1): PWA - manifest, service worker e icones servidos de
verdade pelo app, com conteudo valido (nao so arquivos no disco).
"""
import json
import os

from fastapi.testclient import TestClient

os.environ.setdefault("NVIDIA_API_KEY", "dummy-test-key")
import app_core

_client = TestClient(app_core.create_app())


def test_index_links_manifest_and_registers_service_worker():
    r = _client.get("/")
    assert r.status_code == 200
    assert '<link rel="manifest" href="/manifest.json">' in r.text
    assert "serviceWorker" in r.text
    assert "/sw.js" in r.text


def test_manifest_served_with_correct_type_and_valid_json():
    r = _client.get("/manifest.json")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/manifest+json")
    body = json.loads(r.text)
    assert body["name"]
    assert body["display"] == "standalone"
    assert len(body["icons"]) >= 2
    for icon in body["icons"]:
        assert icon["src"].startswith("/icons/")


def test_service_worker_served_as_javascript():
    r = _client.get("/sw.js")
    assert r.status_code == 200
    assert "javascript" in r.headers["content-type"]
    assert "install" in r.text and "fetch" in r.text


def test_icons_referenced_in_manifest_actually_exist_and_load():
    manifest = json.loads(_client.get("/manifest.json").text)
    for icon in manifest["icons"]:
        r = _client.get(icon["src"])
        assert r.status_code == 200, icon["src"]
        assert r.headers["content-type"] == "image/png"
        assert r.content[:8] == b"\x89PNG\r\n\x1a\n"  # assinatura PNG real


def test_icon_path_rejects_traversal():
    r = _client.get("/icons/..%2f..%2fapp_core.py")
    assert r.status_code == 404
