"""Focused business integration tests; isolated storage and read-only Meta fixtures."""
import json
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import business_workspace as bw


@pytest.fixture
def setup(tmp_path):
    state={'email':'owner@example.test','calls':[], 'incomplete':False}
    def mcp(name,args,email):
        state['calls'].append((name,args,email))
        data={'list_ad_accounts':{'ad_accounts':[{'account_id':'123','currency':'BRL'}]},
              'list_objects':{'items':[{'id':'10'},{'id':'20'}]},
              'get_insights':{'incomplete':state['incomplete'],'rows':[
                  {'campaign_id':'10','spend':'50','impressions':'1000','clicks':'20',
                   'actions':[{'action_type':'purchase','value':'2'},{'action_type':'omni_purchase','value':'2'}],
                   'action_values':[{'action_type':'purchase','value':'300'}]},
                  {'campaign_id':'20','spend':'999','impressions':'999','clicks':'999'}]}}[name]
        return {'content':[{'type':'text','text':json.dumps(data)}]}
    app=FastAPI()
    @app.middleware('http')
    async def auth(request,call_next):
        request.state.user_email=state['email']
        return await call_next(request)
    bw.register(app,{'sb':None,'target':lambda:(None,None),'directory':lambda:tmp_path,'mcp':mcp})
    p={'name':'Produto','price':97,'currency':'BRL','account_id':'123','campaign_ids':['10'],
       'unit_cost':10,'fee_pct':5,'fee_fixed':2,'tax_pct':3,'other_costs':1,'margin_pct':20}
    return TestClient(app),state,p


def test_real_attributed_values_and_readonly_tools(setup):
    c,state,p=setup
    pid=c.post('/api/workspace/products',json=p).json()['product']['id']
    d=c.post('/api/workspace/context',json={'product_id':pid}).json()
    assert d['metrics']['spend']==50
    assert d['metrics']['purchases']==2
    assert d['metrics']['revenue']==300  # not price * purchases, nor another product
    assert d['financial']['net_profit_attributed']==200
    assert d['financial']['received_revenue'] is None
    assert [x[0] for x in state['calls']]==['list_ad_accounts','list_objects','get_insights']


def test_owner_isolation_and_update(setup):
    c,state,p=setup
    pid=c.post('/api/workspace/products',json=p).json()['product']['id']
    state['email']='another@example.test'
    assert c.get('/api/workspace/products').json()['products']==[]
    assert c.post('/api/workspace/products',json={**p,'id':pid}).status_code==404
    assert c.post('/api/workspace/context',json={'product_id':pid}).status_code==404


@pytest.mark.parametrize('patch',[{'fee_pct':101},{'unit_cost':True},{'price':0},
    {'account_id':'act_123'},{'campaign_ids':['invalid']},{'url':'javascript:alert(1)'}])
def test_invalid_profile(setup,patch):
    c,_,p=setup
    assert c.post('/api/workspace/products',json={**p,**patch}).status_code==400


def test_foreign_account_rejected(setup):
    c,_,p=setup
    pid=c.post('/api/workspace/products',json=p).json()['product']['id']
    assert c.post('/api/workspace/context',json={'product_id':pid,'account_id':'999'}).status_code==403


def test_product_context_remains_available_before_meta_connection(setup):
    c,state,p=setup
    p['account_id']=''
    pid=c.post('/api/workspace/products',json=p).json()['product']['id']
    response=c.post('/api/workspace/context',json={'product_id':pid})
    assert response.status_code==200
    assert response.json()['product']['name']=='Produto'
    assert response.json()['metrics'] is None
    assert state['calls']==[]


def test_missing_costs_not_invented(setup):
    c,_,p=setup
    p.pop('unit_cost')
    pid=c.post('/api/workspace/products',json=p).json()['product']['id']
    d=c.post('/api/workspace/context',json={'product_id':pid}).json()
    assert d['financial']=={'status':'costs_required','missing':['unit_cost']}


def test_currency_and_truncation_prevent_wrong_totals(setup):
    c,state,p=setup
    p['currency']='USD'
    pid=c.post('/api/workspace/products',json=p).json()['product']['id']
    assert c.post('/api/workspace/context',json={'product_id':pid}).json()['metrics'] is None
    p['currency']='BRL'
    c.post('/api/workspace/products',json={**p,'id':pid})
    state['incomplete']=True
    assert c.post('/api/workspace/context',json={'product_id':pid}).json()['metrics'] is None


def test_existing_supabase_schema_and_owner_filters(tmp_path):
    stored=[]
    queries=[]
    def sb(method,table,params=None,payload=None):
        assert table=='ad_drafts'
        queries.append((method,params,payload))
        if method=='POST':
            stored[:]=[r for r in stored if r['id']!=payload['id']]+[payload]
            return None
        return [r for r in stored if params['owner_email']=='eq.'+r['owner_email'] and params['structure_slug']=='eq.'+r['structure_slug']]
    app=FastAPI()
    @app.middleware('http')
    async def auth(request,call_next):
        request.state.user_email='schema@example.test'
        return await call_next(request)
    bw.register(app,{'sb':sb,'target':lambda:('https://fixture.invalid','not-a-key'),
                     'directory':lambda:tmp_path,'mcp':lambda *a:None})
    c=TestClient(app)
    saved=c.post('/api/workspace/products',json={'name':'Existing schema'}).json()['product']
    assert c.get('/api/workspace/products').json()['products'][0]['id']==saved['id']
    assert set(stored[0])=={'id','owner_email','structure_slug','structure_name','briefing','updated_at'}
    assert all(q[1]['owner_email']=='eq.schema@example.test' for q in queries if q[0]=='GET')
