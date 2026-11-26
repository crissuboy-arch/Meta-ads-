"""Hubla endpoint tests: no live payments, network or customer records."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import hubla_access


def sale():
    return {'version': '2.0.0', 'type': 'invoice.payment_succeeded', 'event': {
        'products': [{'id': 'launch-product'}], 'user': {'email': 'Buyer@example.test'},
        'invoice': {'id': 'invoice-test', 'version': 2, 'status': 'paid',
                    'currency': 'BRL', 'amount': {'totalCents': 9700}}}}


@pytest.fixture
def endpoint(monkeypatch):
    monkeypatch.setenv('HUBLA_WEBHOOK_TOKEN', 'test-only-token')
    monkeypatch.setenv('HUBLA_PRODUCT_ID', 'launch-product')
    monkeypatch.delenv('HUBLA_LIVE_ACCESS_ENABLED', raising=False)
    monkeypatch.delenv('HUBLA_ACCESS_MODEL', raising=False)
    calls = []
    app = FastAPI()
    hubla_access.register(app, lambda *args, **kwargs: calls.append((args, kwargs)))
    headers = {'x-hubla-token': 'test-only-token', 'x-hubla-sandbox': 'true',
               'x-hubla-idempotency': 'receipt-1', 'x-hubla-delivery-mode': 'standard'}
    return TestClient(app), headers, calls


def test_official_sandbox_never_writes(endpoint):
    client, headers, calls = endpoint
    result = client.post('/api/webhooks/hubla', headers=headers, json=sale())
    assert result.status_code == 200 and result.json()['access_changed'] is False
    assert calls == []


@pytest.mark.parametrize('header,value,expected', [
    ('x-hubla-token', 'wrong', 401), ('x-hubla-sandbox', '', 400),
    ('x-hubla-idempotency', '', 400), ('x-hubla-delivery-mode', 'compatibility', 400)])
def test_required_headers(endpoint, header, value, expected):
    client, headers, calls = endpoint
    headers[header] = value
    assert client.post('/api/webhooks/hubla', headers=headers, json=sale()).status_code == expected
    assert not calls


def test_missing_configuration_fails_closed(endpoint, monkeypatch):
    client, headers, calls = endpoint
    monkeypatch.delenv('HUBLA_WEBHOOK_TOKEN')
    assert client.post('/api/webhooks/hubla', headers=headers, json=sale()).status_code == 503
    assert not calls


def test_live_disabled_by_default_and_unknown_access_model(endpoint, monkeypatch):
    client, headers, calls = endpoint
    headers['x-hubla-sandbox'] = 'false'
    assert client.post('/api/webhooks/hubla', headers=headers, json=sale()).status_code == 503
    monkeypatch.setenv('HUBLA_LIVE_ACCESS_ENABLED', 'true')
    assert client.post('/api/webhooks/hubla', headers=headers, json=sale()).status_code == 503
    assert not calls


def test_paid_and_refunded_use_same_transactional_rpc(endpoint, monkeypatch):
    client, headers, calls = endpoint
    monkeypatch.setenv('HUBLA_LIVE_ACCESS_ENABLED', 'true')
    monkeypatch.setenv('HUBLA_ACCESS_MODEL', 'one_time')
    headers['x-hubla-sandbox'] = 'false'
    body = sale()
    assert client.post('/api/webhooks/hubla', headers=headers, json=body).status_code == 200
    # Canonical hash is insensitive to JSON property ordering.
    assert client.post('/api/webhooks/hubla', headers=headers, json=dict(reversed(list(body.items())))).status_code == 200
    assert calls[0][1]['payload']['p_hash'] == calls[1][1]['payload']['p_hash']
    body['type'] = 'invoice.refunded'
    body['event']['invoice'].update(status='refunded', version=3)
    assert client.post('/api/webhooks/hubla', headers=headers, json=body).status_code == 200
    assert calls[-1][0] == ('POST', 'rpc/hubla_apply_event')
    assert calls[-1][1]['payload']['p_email'] == 'buyer@example.test'
    assert calls[-1][1]['payload']['p_status'] == 'refunded'


@pytest.mark.parametrize('field,value', [('status', 'unpaid'), ('version', True),
    ('version', -1), ('currency', 'USD'), ('parentInvoiceId', 'real-parent'),
    ('amount', {'totalCents': 97}), ('amount', {'totalCents': 9700.0})])
def test_invalid_payment_never_grants(endpoint, field, value):
    client, headers, calls = endpoint
    body = sale()
    body['event']['invoice'][field] = value
    assert client.post('/api/webhooks/hubla', headers=headers, json=body).status_code == 400
    assert not calls


def test_other_product_and_pending_events_ignored(endpoint):
    client, headers, calls = endpoint
    body = sale()
    body['event']['products'][0]['id'] = 'unrelated-product'
    assert client.post('/api/webhooks/hubla', headers=headers, json=body).json()['ignored']
    body = sale()
    body['type'] = 'invoice.payment_failed'
    assert client.post('/api/webhooks/hubla', headers=headers, json=body).json()['ignored']
    assert not calls


def test_db_failure_is_retryable(monkeypatch):
    monkeypatch.setenv('HUBLA_WEBHOOK_TOKEN', 'token')
    monkeypatch.setenv('HUBLA_PRODUCT_ID', 'launch-product')
    monkeypatch.setenv('HUBLA_LIVE_ACCESS_ENABLED', 'true')
    monkeypatch.setenv('HUBLA_ACCESS_MODEL', 'one_time')
    app = FastAPI()
    def unavailable(*args, **kwargs):
        raise RuntimeError('database offline')
    hubla_access.register(app, unavailable)
    response = TestClient(app).post('/api/webhooks/hubla', json=sale(), headers={
        'x-hubla-token': 'token', 'x-hubla-sandbox': 'false',
        'x-hubla-idempotency': 'receipt', 'x-hubla-delivery-mode': 'standard'})
    assert response.status_code == 503


def test_legacy_access_precedes_hubla(monkeypatch):
    import app_core
    monkeypatch.setattr(app_core, '_sb_target', lambda: ('test', 'test'))
    calls = []
    def request(method, table, **kwargs):
        calls.append(table)
        return [{'status': 'active'}]
    monkeypatch.setattr(app_core, '_sb_req', request)
    assert app_core._buyer_is_active('legacy@example.test')
    assert calls == ['app_buyers']
