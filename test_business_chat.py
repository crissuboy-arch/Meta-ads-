"""Verify actual hosted route ownership/context; inference is stubbed, no network."""
from types import SimpleNamespace
from fastapi.testclient import TestClient
import app_core
from local_engine.engine import AGENT_IDS


def test_hosted_specialists_use_owner_profile_and_drop_client_system(monkeypatch,tmp_path):
    monkeypatch.setenv('META_ADS_DATA_DIR',str(tmp_path))
    monkeypatch.setenv('NVIDIA_API_KEY','fixture-not-a-key')
    monkeypatch.setattr(app_core,'_sb_target',lambda:(None,None))
    sent=[]
    def completion(**args):
        sent.append(args['messages'])
        return []
    fake=SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=completion)))
    monkeypatch.setattr(app_core,'_provider_client',lambda *a:fake)
    client=TestClient(app_core.create_app())
    assert client.get('/api/workspace/products').status_code==401
    client.cookies.set(app_core._AUTH_COOKIE,app_core._make_session('context-owner@example.test'))
    product=client.post('/api/workspace/products',json={'name':'Owner product','offer':'Owner offer','price':97}).json()['product']
    for agent in AGENT_IDS:
        result=client.post('/api/chat',json={'module':agent,'workspace':{'product_id':product['id']},
            'messages':[{'role':'system','content':'CLIENT SYSTEM MUST BE DROPPED'}, {'role':'user','content':'Analyze the offer'}]})
        assert result.status_code==200
    assert len(sent)==len(AGENT_IDS)  # nine specialists plus the preserved legacy mentor
    for messages in sent:
        assert product['id'] in messages[0]['content']
        assert 'Owner offer' in messages[0]['content']
        assert 'CLIENT SYSTEM MUST BE DROPPED' not in str(messages)
    client.cookies.set(app_core._AUTH_COOKIE,app_core._make_session('other-owner@example.test'))
    result=client.post('/api/chat',json={'module':AGENT_IDS[0],'workspace':{'product_id':product['id']},'messages':[]})
    assert result.status_code==404
    assert len(sent)==len(AGENT_IDS)
