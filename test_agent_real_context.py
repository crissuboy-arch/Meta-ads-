"""Verify MCP read routing/ownership without external requests."""
import app_core


def test_agent_context_uses_authenticated_owner_and_caches_only_same_owner(monkeypatch):
    calls=[]
    app_core._AGENT_CONTEXT_CACHE.clear()
    def call(name,args,email):
        calls.append((name,args,email))
        return {'content':[{'type':'text','text':email+' metrics'}]}
    monkeypatch.setattr(app_core,'_mcp_tool_call',call)
    first=app_core._agent_read_context('analista-financeiro','owner-a@example.test')
    again=app_core._agent_read_context('analista-financeiro','owner-a@example.test')
    other=app_core._agent_read_context('analista-financeiro','owner-b@example.test')
    assert first == again and 'owner-a' not in other
    assert len(calls) == 2 and all(c[0] == 'account_overview' for c in calls)
    assert calls[0][2] == 'owner-a@example.test'
    app_core._AGENT_CONTEXT_CACHE.clear()


def test_missing_context_is_reported_and_unrelated_modules_do_not_call_mcp(monkeypatch):
    monkeypatch.setattr(app_core,'_mcp_tool_call',lambda *a:{'isError':True})
    assert 'indisponiveis' in app_core._agent_read_context('auditor-campanhas','none@example.test')
    assert app_core._agent_read_context('copy','owner@example.test') is None
    assert app_core._agent_read_context('auditor-campanhas',None) is None
