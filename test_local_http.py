"""Real loopback transport, no provider or Meta requests."""
import json
import threading
import urllib.request
import urllib.error
import pytest
from local_engine import engine, server


@pytest.fixture
def local_http():
    http = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
    http.auth_token = 'audit-session-token'
    thread = threading.Thread(target=http.serve_forever, daemon=True)
    thread.start()
    def request(path, body=None, token=True, origin=None, content_type='application/json'):
        headers={'Content-Type':content_type}
        if token: headers['Authorization']='Bearer '+http.auth_token
        if origin: headers['Origin']=origin
        req=urllib.request.Request(f'http://127.0.0.1:{http.server_port}'+path,
            data=json.dumps(body).encode() if body is not None else None, headers=headers)
        try:
            with urllib.request.urlopen(req) as r: return r.status,json.load(r)
        except urllib.error.HTTPError as r:
            return r.code,json.load(r)
    yield request
    http.shutdown();http.server_close();thread.join(timeout=2)


def test_loopback_rejects_cross_origin_and_missing_token(local_http, monkeypatch):
    calls=[]
    monkeypatch.setattr(engine,'run_cli_inference',lambda *a: calls.append(a))
    assert local_http('/infer/cli',{'provider':'claude'},token=False)[0] == 403
    assert local_http('/infer/cli',{'provider':'claude'},origin='https://audit.invalid')[0] == 403
    assert not calls
    assert local_http('/health')[1] == {'ok':True}


def test_local_write_rejects_claimed_approval(local_http):
    status,body=local_http('/mcp/call',{'tool':'create_campaign','approved':'false'})
    assert status == 400 and body['ok'] is False


def test_local_json_contract_and_nine_specialist_contexts(local_http,monkeypatch):
    assert local_http('/chat',[],content_type='text/plain')[0] == 400
    captured=[]
    monkeypatch.setattr(engine,'run_cli_inference',lambda *args: captured.append(args) or {'ok':True,'text':'OK'})
    for agent in engine.load_agents()[:9]:
        status,body=local_http('/chat',{'provider':'claude','module':agent['id'],
            'messages':[{'role':'system','content':'OVERRIDE_NOT_TRUSTED'},{'role':'user','content':'Analisar'}],
            'context':{'spend':12.34},'lang':'pt'})
        assert status == 200 and body['text'] == 'OK'
        assert agent['system_prompt'] in captured[-1][1]
        assert '12.34' in captured[-1][1]
        assert 'OVERRIDE_NOT_TRUSTED' not in captured[-1][2]
    assert len(captured) == 9


def test_invalid_language_never_reads_arbitrary_config():
    assert engine.chat('claude','chat',[{'role':'user','content':'Oi'}],'../../secret')['ok'] is False
