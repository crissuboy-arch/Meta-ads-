"""Regression coverage for existing payment notifications, Pixel config and CAPI.

All storage is temporary and all Graph API transport is mocked. No live checkout,
payment, Supabase record or production credential is touched.
"""
import hashlib
import hmac
import json
import os
import time
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault('NVIDIA_API_KEY','dummy-test-key')
import app_core

KEY='a'*32

@pytest.fixture
def local(monkeypatch,tmp_path):
    monkeypatch.setenv('META_ADS_DATA_DIR',str(tmp_path))
    monkeypatch.delenv('CAKTO_WEBHOOK_SECRET',raising=False)
    monkeypatch.delenv('APP_ADMIN_EMAILS',raising=False)
    monkeypatch.setattr(app_core,'_sb_target',lambda:(None,None))
    calls=[]
    def post(url,**kwargs):
        calls.append((url,kwargs))
        return SimpleNamespace(status_code=200)
    monkeypatch.setattr(app_core,'_requests',SimpleNamespace(post=post))
    client=TestClient(app_core.create_app())
    result=client.post('/api/auth/register',json={'email':'checkout-test@example.test','password':'Local-checkout-tests-only!'})
    assert result.status_code==200
    return client,calls

def payload(event='purchase_approved',method='pix'):
    return {'event':event,'data':{'id':'order-test','refId':'reference-test',
        'paymentMethod':method,'amount':129.90,'currency':'BRL',
        'utm_source':'test-source','utm_campaign':'test-campaign',
        'customer':{'email':'buyer@example.test','phone':'+5511999990000','name':'Test Buyer'}}}

@pytest.mark.parametrize('method,normalized',[('pix','pix'),('credit_card','card'),('boleto','boleto')])
def test_cakto_paid_webhook_preserves_payment_method_and_amount(local,method,normalized):
    client,calls=local
    response=client.post('/api/webhooks/sales/'+KEY,json=payload(method=method))
    assert response.status_code==200
    assert response.json()['capi_event']=='Purchase'
    assert response.json()['capi_status']=='no_credentials'
    sale=client.get('/api/sales',params={'key':KEY}).json()['sales'][0]
    assert (sale['platform'],sale['method'],sale['amount'],sale['currency'])==('cakto',normalized,129.90,'BRL')
    assert sale['utm_campaign']=='test-campaign'
    assert not calls

@pytest.mark.parametrize('event,method,expected',[
    ('pix_gerado','pix','InitiateCheckout'),('boleto_gerado','boleto','AddPaymentInfo'),
    ('picpay_gerado','picpay','InitiateCheckout')])
def test_pending_checkout_is_not_recorded_as_paid(local,event,method,expected):
    client,_=local
    response=client.post('/api/webhooks/sales/'+KEY,json=payload(event,method))
    assert response.json()['capi_event']==expected
    assert client.get('/api/sales',params={'key':KEY}).json()['sales'][0]['status']=='pending'

@pytest.mark.parametrize('event',['pix_expirado','purchase_refused','refund','chargeback','checkout_abandonment','initiate_checkout'])
def test_cakto_ignored_events_retain_original_behavior(local,event):
    client,calls=local
    response=client.post('/api/webhooks/sales/'+KEY,json=payload(event))
    assert response.status_code==200 and response.json()['ignored'] is True
    assert client.get('/api/sales',params={'key':KEY}).json()['total']==0
    assert not calls

def test_duplicate_notification_does_not_duplicate_sale_or_capi_send(local):
    client,calls=local
    app_core._store_put_config(KEY,{'pixel_id':'123456789012345','token':'test-token'},None)
    first=client.post('/api/webhooks/sales/'+KEY,json=payload()).json()
    second=client.post('/api/webhooks/sales/'+KEY,json=payload()).json()
    assert first['capi_status']=='sent' and second['duplicate'] is True
    assert client.get('/api/sales',params={'key':KEY}).json()['total']==1
    assert len(calls)==1

def test_capi_receives_hashed_customer_data_value_currency_and_same_event_id(local):
    client,calls=local
    app_core._store_put_config(KEY,{'pixel_id':'123456789012345','token':'test-token'},None)
    response=client.post('/api/webhooks/sales/'+KEY,json=payload()).json()
    assert response['capi_status']=='sent'
    url,kwargs=calls[0]
    assert url.endswith('/123456789012345/events')
    sent=kwargs['json']['data'][0]
    assert sent['event_id']==response['sale_id']
    assert sent['custom_data']['value']==129.90 and sent['custom_data']['currency']=='BRL'
    assert sent['user_data']['em']==[hashlib.sha256(b'buyer@example.test').hexdigest()]
    stored=app_core._trk_load()[KEY]['sales'][0]
    assert 'buyer@example.test' not in json.dumps(stored)
    assert 'test-token' not in json.dumps(stored)

def test_cakto_rejects_wrong_secret_and_accepts_valid_secret(local,monkeypatch):
    client,_=local;monkeypatch.setenv('CAKTO_WEBHOOK_SECRET','local-test-secret')
    body=payload()
    assert client.post('/api/webhooks/sales/'+KEY,json=body).status_code==401
    body['secret']='local-test-secret'
    assert client.post('/api/webhooks/sales/'+KEY,json=body).status_code==200

def test_cakto_signature_validates_body_and_timestamp(local,monkeypatch):
    client,_=local;monkeypatch.setenv('CAKTO_WEBHOOK_SECRET','local-test-secret')
    raw=json.dumps(payload()).encode();ts=str(int(time.time()))
    sig='v1='+hmac.new(b'local-test-secret',ts.encode()+b'.'+raw,hashlib.sha256).hexdigest()
    headers={'x-cakto-timestamp':ts,'x-cakto-signature':sig,'content-type':'application/json'}
    assert client.post('/api/webhooks/sales/'+KEY,content=raw,headers=headers).status_code==200
    headers['x-cakto-timestamp']='1'
    assert client.post('/api/webhooks/sales/'+KEY,content=raw,headers=headers).status_code==401

def test_pixel_configuration_and_token_privacy_are_preserved(local):
    client,_=local
    response=client.post('/api/tracking/config',json={'key':KEY,'pixel_id':'123456789012345',
        'token':'pixel-token-must-stay-server-side','domain':'https://example.test/path',
        'events':['PageView','Purchase','Lead']})
    assert response.status_code==200
    data=client.get('/api/tracking/config',params={'key':KEY})
    assert data.json()['has_token'] is True
    assert data.json()['domain']=='example.test'
    assert data.json()['events']==['PageView','Purchase','Lead']
    assert 'pixel-token-must-stay-server-side' not in response.text+data.text

def test_hotmart_access_grant_and_revocation_are_preserved(local,monkeypatch):
    client,_=local;monkeypatch.setenv('HOTMART_HOTTOK','local-test-hottok')
    body={'event':'PURCHASE_APPROVED','data':{'buyer':{'email':'buyer@example.test'}}}
    assert client.post('/api/webhooks/hotmart',json=body).status_code==401
    headers={'x-hotmart-hottok':'local-test-hottok'}
    assert client.post('/api/webhooks/hotmart',json=body,headers=headers).json()['status']=='active'
    assert app_core._buyer_is_active('buyer@example.test')
    body['event']='PURCHASE_REFUNDED'
    assert client.post('/api/webhooks/hotmart',json=body,headers=headers).json()['status']=='inactive'
    assert not app_core._buyer_is_active('buyer@example.test')
