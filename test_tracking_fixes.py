"""Fase V: correcoes de rastreamento/pagamentos encontradas na investigacao
pos-redesign (docs/PENDENCIAS-ANTERIORES-CAPI-PAGAMENTOS.txt).

1) O webhook de RASTREAMENTO de vendas da Hotmart (/api/webhooks/sales/{key})
   nao verificava nenhuma assinatura - so o webhook de ACESSO ao produto
   verificava HOTMART_HOTTOK. Agora, quando HOTMART_HOTTOK esta configurado
   e o payload tem o formato da Hotmart, a assinatura passa a ser exigida.
2) Hotmart/Stripe/Kiwify/generic sempre caiam no uuid aleatorio de
   event_id (so a Cakto tinha id estavel) - um reenvio de webhook (comum
   nesses provedores) nunca era detectado como duplicata e reenviava
   Purchase pro Meta. Agora usam um id estavel derivado da transacao real.

Toda chamada ao Meta e mockada - nenhum envio real, nenhuma venda
fictícia em produção, nenhuma campanha tocada.
"""
import os
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault('NVIDIA_API_KEY', 'dummy-test-key')
import app_core

KEY = 'b' * 32


@pytest.fixture
def local(monkeypatch, tmp_path):
    monkeypatch.setenv('META_ADS_DATA_DIR', str(tmp_path))
    monkeypatch.delenv('CAKTO_WEBHOOK_SECRET', raising=False)
    monkeypatch.delenv('HOTMART_HOTTOK', raising=False)
    monkeypatch.delenv('APP_ADMIN_EMAILS', raising=False)
    monkeypatch.setattr(app_core, '_sb_target', lambda: (None, None))
    calls = []

    def post(url, **kwargs):
        calls.append((url, kwargs))
        return SimpleNamespace(status_code=200)

    monkeypatch.setattr(app_core, '_requests', SimpleNamespace(post=post))
    client = TestClient(app_core.create_app())
    result = client.post('/api/auth/register',
                          json={'email': 'tracking-fixes@example.test',
                                'password': 'Local-tracking-tests-only!'})
    assert result.status_code == 200
    return client, calls


def hotmart_payload(status='APPROVED', transaction='HP123456789012345'):
    return {
        'event': 'PURCHASE_COMPLETE',
        'data': {
            'purchase': {
                'transaction': transaction,
                'status': status,
                'price': {'value': 199.90, 'currency_code': 'BRL'},
                'payment': {'type': 'CREDIT_CARD'},
            },
            'buyer': {'email': 'buyer@example.test', 'name': 'Test Buyer',
                      'checkout_phone': '+5511999990000'},
        },
    }


def test_hotmart_tracking_webhook_works_unchanged_when_hottok_not_configured(local):
    """Regressao: contas que ainda nao configuraram HOTMART_HOTTOK para o
    rastreamento continuam funcionando exatamente como antes."""
    client, _ = local
    response = client.post('/api/webhooks/sales/' + KEY, json=hotmart_payload())
    assert response.status_code == 200
    assert response.json()['capi_event'] == 'Purchase'


def test_hotmart_tracking_webhook_rejects_wrong_or_missing_signature_when_configured(local, monkeypatch):
    client, _ = local
    monkeypatch.setenv('HOTMART_HOTTOK', 'local-test-hottok')
    response = client.post('/api/webhooks/sales/' + KEY, json=hotmart_payload())
    assert response.status_code == 401
    response = client.post('/api/webhooks/sales/' + KEY, json=hotmart_payload(),
                            headers={'x-hotmart-hottok': 'wrong'})
    assert response.status_code == 401


def test_hotmart_tracking_webhook_accepts_valid_signature_when_configured(local, monkeypatch):
    client, _ = local
    monkeypatch.setenv('HOTMART_HOTTOK', 'local-test-hottok')
    response = client.post('/api/webhooks/sales/' + KEY, json=hotmart_payload(),
                            headers={'x-hotmart-hottok': 'local-test-hottok'})
    assert response.status_code == 200
    assert response.json()['capi_event'] == 'Purchase'


def test_hotmart_signature_requirement_never_affects_cakto_payloads(local, monkeypatch):
    """A nova verificacao e especifica do formato Hotmart (data.purchase) -
    payloads da Cakto continuam passando sem x-hotmart-hottok nenhum."""
    client, _ = local
    monkeypatch.setenv('HOTMART_HOTTOK', 'local-test-hottok')
    cakto_body = {'event': 'purchase_approved', 'data': {
        'id': 'order-test', 'paymentMethod': 'pix', 'amount': 50.0, 'currency': 'BRL',
        'customer': {'email': 'buyer@example.test'}}}
    response = client.post('/api/webhooks/sales/' + KEY, json=cakto_body)
    assert response.status_code == 200


def test_hotmart_event_id_is_stable_and_derived_from_the_real_transaction(local):
    client, calls = local
    app_core._store_put_config(KEY, {'pixel_id': '123456789012345', 'token': 'test-token'}, None)
    response = client.post('/api/webhooks/sales/' + KEY, json=hotmart_payload()).json()
    assert response['sale_id'] == 'hotmart-HP123456789012345-paid'
    assert response['capi_status'] == 'sent'
    assert len(calls) == 1


def test_hotmart_webhook_retry_does_not_duplicate_sale_or_resend_capi(local):
    """Antes desta correcao, um reenvio de webhook (comum em Hotmart por
    timeout) nunca era detectado como duplicata - cada reenvio inseria
    outra venda e reenviava Purchase pro Meta."""
    client, calls = local
    app_core._store_put_config(KEY, {'pixel_id': '123456789012345', 'token': 'test-token'}, None)
    first = client.post('/api/webhooks/sales/' + KEY, json=hotmart_payload()).json()
    second = client.post('/api/webhooks/sales/' + KEY, json=hotmart_payload()).json()
    assert first['capi_status'] == 'sent'
    assert second.get('duplicate') is True
    assert client.get('/api/sales', params={'key': KEY}).json()['total'] == 1
    assert len(calls) == 1


def test_generic_platform_also_gets_a_stable_event_id_when_an_id_is_present(local):
    client, _ = local
    body = {'id': 'txn-999', 'status': 'paid', 'amount': 75.0, 'currency': 'BRL',
            'email': 'buyer@example.test'}
    response = client.post('/api/webhooks/sales/' + KEY, json=body).json()
    assert response['sale_id'] == 'generic-txn-999-paid'
