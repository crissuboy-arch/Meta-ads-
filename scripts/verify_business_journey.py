"""Local browser integration checks. Meta/AI are explicit fixtures; no live writes."""
import json
import os
import uuid
from pathlib import Path
from playwright.sync_api import sync_playwright

checks=[]
def ok(label):
    checks.append(label)
    print('PASS:',label,flush=True)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('BROWSER_EXE',r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'))
    page=browser.new_page(viewport={'width':1440,'height':1100},service_workers='block')
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.add_init_script("localStorage.setItem('metaAdsLang','pt')")
    page.goto('http://127.0.0.1:8831/',wait_until='networkidle')
    email='integration-'+uuid.uuid4().hex[:12]+'@ofensiva.test'
    registration=page.request.post('http://127.0.0.1:8831/api/auth/register',data={'email':email,'password':'Test-Local-2026!'})
    assert registration.status==200
    page.reload(wait_until='networkidle')
    page.locator('#authOverlay.hidden').wait_for(state='attached')
    page.wait_for_function('typeof BF!=="undefined" && BF.ready')
    ok('Real existing local authentication and workspace endpoint')
    def nav(name):
        page.locator('#sideNav [data-id="'+name+'"]').click()
    nav('products')
    page.locator('#bfProductForm').wait_for()
    assert page.locator('#importsSection').count()==1
    page.locator('#bf-name').fill('Produto de teste local — não é conta real')
    for key,value in {'price':'97','unit_cost':'10','fee_pct':'5','fee_fixed':'2','tax_pct':'3','other_costs':'1','margin_pct':'20'}.items():
        page.locator('#bf-'+key).fill(value)
    page.locator('#bf-url').fill('https://example.com/produto')
    page.locator('#bf-offer').fill('Oferta de teste, validada somente em ambiente isolado.')
    page.locator('#bfProductForm [type="submit"]').click()
    page.wait_for_function('BF.product?.name.startsWith("Produto de teste")')
    pid=page.evaluate('BF.product.id')
    page.reload(wait_until='networkidle')
    page.wait_for_function('typeof BF!=="undefined" && BF.ready')
    assert page.evaluate('BF.product.id')==pid
    ok('Product and costs persist via real authenticated isolated storage; imports retained')
    # External services below are fixtures, never credentials or a real campaign.
    calls=[]
    syncs=[]
    def ads(route):
        path=route.request.url.split('/api/ads/')[-1]
        body=route.request.post_data_json if route.request.method=='POST' else {}
        if path=='status':out={'connected':True,'accounts':[{'account_id':'123','name':'FIXTURE Meta','selected':True,'currency':'BRL'}]}
        elif path=='wizard/meta':out={'objectives':['OUTCOME_SALES','OUTCOME_TRAFFIC'],'write_actions_enabled':False}
        elif path=='wizard/call':
            calls.append(body)
            out={'list_objects':{'items':[{'id':'10','name':'FIXTURE campanha'}]},'list_pages':{'pages':[{'id':'88','name':'FIXTURE página'}]},'list_pixels':{'pixels':[{'id':'123456789012','name':'FIXTURE Pixel'}]}}.get(body.get('tool'),{})
        else:
            if path=='sync':syncs.append(body)
            out={'ok':True,'errors':[],'campaigns':[],'totals':{}}
        route.fulfill(json=out)
    page.route('**/api/ads/**',ads)
    nav('ads-connect')
    page.locator('#bfMetaGuide').wait_for()
    page.wait_for_function('bfSyncAt>0')
    assert len(syncs)==1 and syncs[0]['days']==7
    ok('Connected selected accounts trigger automatic data import (Meta fixture)')
    page.evaluate("async()=>{await bfSave({...BF.product,account_id:'123',campaign_ids:['10']})}")
    fixture={'read_only':True,'product':page.evaluate('BF.product'),'account':{'account_id':'123','currency':'BRL'},'campaigns':[{'id':'10'}],'preset':'today','errors':[],
        'metrics':{'spend':50,'revenue':300,'purchases':2,'cpc':2.5,'cpm':50,'ctr':2},
        'financial':{'status':'estimated_from_attribution','net_profit_attributed':200,'roi':200,'roas':6,'cpa':25,'max_cpa':57.84,'breakeven_roas':1.26,'received_revenue':None}}
    page.route('**/api/workspace/context',lambda r:r.fulfill(json=fixture))
    nav('finance')
    page.locator('#bfFinanceLive .metric-grid').wait_for()
    assert page.locator('#finSpend').input_value()=='50'
    assert page.locator('#finPurchases').input_value()=='2'
    assert page.locator('#finSpend').get_attribute('readonly') is not None
    assert page.locator('#bfFinanceLive').inner_text().find('Não apurada aqui')>=0
    ok('Financial fields use selected campaign values; cash and attribution are distinguished (Meta fixture)')
    nav('rastreamento')
    page.locator('#bfTrackingGuide').wait_for()
    page.locator('#bfFindPixels').click()
    page.locator('#bfPixelChoices button').click()
    assert page.locator('#trkPixel').input_value()=='123456789012'
    page.locator('[data-tracking-step="2"]').click()
    assert page.locator('#trkCopyScript').is_visible()
    assert '123456789012' in page.locator('#trkScript').inner_text()
    page.locator('[data-tracking-step="3"]').click()
    page.locator('#trkSendTest').click()
    assert 'TEST' in page.locator('#trkMsg').inner_text()
    ok('Pixel selection, original script/copy handlers and TEST-code guard (Meta fixture)')
    nav('campwiz')
    page.locator('#bfCampaignJourney').wait_for()
    for step in range(2,7):
        page.locator('[data-campaign-step="'+str(step)+'"]').click()
        page.wait_for_function('(step)=>BC.step===step',arg=step)
        if step==2:
            page.locator('#bc-name').fill('FIXTURE — não publicar')
            page.locator('#bc-objective').select_option('OUTCOME_SALES')
        elif step==4:
            page.locator('#bc-headline').fill('Título revisado')
            page.locator('#bc-message').fill('Texto revisado pelo utilizador')
        elif step==5:
            page.locator('#bc-image_url').fill('https://example.com/image.png')
            page.locator('#bc-page_id').select_option('88')
            page.locator('#bc-pixel_id').select_option('123456789012')
        elif step==6:page.locator('#bc-budget').fill('25')
    page.locator('[data-campaign-step="8"]').click()
    page.locator('#bcCreate').wait_for()
    assert page.locator('#bcCreate').is_disabled()
    assert not any(c['tool'].startswith('create_') for c in calls)
    assert page.evaluate('BF.product.draft.budget')==25
    ok('All campaign stages save through the real endpoint; server write gate stays disabled')
    # Enable only the fixture's UI metadata, never the actual server environment.
    def create_fixture(route):
        payload=route.request.post_data_json
        calls.append(payload)
        assert payload['human_confirmed'] is True
        key={'create_campaign':'campaign_id','create_adset':'adset_id','create_ad':'ad_id'}[payload['tool']]
        route.fulfill(json={key:{'campaign_id':'100','adset_id':'200','ad_id':'300'}[key],'status':'PAUSED'})
    page.route('**/api/ads/wizard/call',create_fixture)
    page.evaluate('()=>{cwMeta.write_actions_enabled=true;bcRender()}')
    page.locator('#bcCreate').click()
    assert 'Confirme' in page.locator('#bcMessage').inner_text()
    assert not any(c['tool'].startswith('create_') for c in calls)
    page.on('dialog',lambda d:d.accept())
    page.locator('#bcApprove').check()
    page.locator('#bcCreate').click()
    page.wait_for_function('BF.product.draft.ad_id==="300"')
    writes=[c for c in calls if c['tool'].startswith('create_')]
    assert len(writes)==3
    assert page.evaluate('BF.product.draft.campaign_id')=='100'
    assert '100' in page.evaluate('BF.product.campaign_ids')
    assert page.locator('#bcCreate').is_disabled()
    assert all(c['tool']!='set_status' for c in calls)
    ok('Explicit approval creates all three stages once, retains IDs, never activates (Meta fixture only)')
    def fail_fixture(route):
        payload=route.request.post_data_json
        calls.append(payload)
        if payload['tool']=='create_campaign':route.fulfill(json={'campaign_id':'101','status':'PAUSED'})
        else:route.fulfill(status=503,json={'detail':'FIXTURE interrupted; result uncertain'})
    page.unroute('**/api/ads/wizard/call',create_fixture)
    page.route('**/api/ads/wizard/call',fail_fixture)
    page.evaluate("()=>{for(const k of ['campaign_id','adset_id','ad_id','created_hash','pending_action'])BC.draft[k]='';bcRender()}")
    page.locator('#bcApprove').check()
    page.locator('#bcCreate').click()
    page.wait_for_function('BC.draft.pending_action==="create_adset" && !BC.locked')
    assert page.evaluate('BF.product.draft.campaign_id')=='101'
    assert page.evaluate('JSON.parse(localStorage.getItem(bcRecoveryKey())).pending_action')=='create_adset'
    assert page.locator('#bcCreate').is_disabled()
    ok('Partial failure retains campaign ID and blocks uncertain retries/duplicates (Meta fixture)')
    # Verify all nine specialists pass the same context through native IPC.
    page.evaluate("""()=>{window.__TAURI__={core:{invoke:async(name,args)=>{window.testNativeCalls=window.testNativeCalls||[];window.testNativeCalls.push({name,args});return {ok:true,text:'FIXTURE OK'}}}};localStorage.setItem('ofensivaLocalProvider','codex')}""")
    result=page.evaluate("""async()=>{const ids=PREMIUM_AGENTS.map(x=>x[0]);for(const id of ids){let text='';await streamChat('',[{role:'user',content:'Teste isolado'}],{onChunk:t=>text+=t,onDone:()=>{}},id);if(text!=='FIXTURE OK')throw new Error(id)}return window.testNativeCalls}""")
    assert len(result)==9
    assert all(r['args']['payload']['context']['product']['id']==pid and r['args']['payload']['context']['metrics']['spend']==50 for r in result)
    ok('All nine specialist calls include product, authorized account, costs and campaign context (native IPC fixture)')
    api_prompts=[]
    def api_fixture(route):
        api_prompts.append(route.request.post_data_json['prompt'])
        route.fulfill(json={'ok':True,'text':'FIXTURE API OK'})
    page.route('**/api/providers/generate',api_fixture)
    page.evaluate("()=>{delete window.__TAURI__;localStorage.removeItem('ofensivaLocalProvider');localStorage.setItem('ofensivaUxAiMode','byok')}")
    page.evaluate("async()=>{await streamChat('',[{role:'user',content:'Teste'}],{onChunk:()=>{},onDone:()=>{}},PREMIUM_AGENTS[0][0])}")
    assert len(api_prompts)==1 and pid in api_prompts[0] and 'BUSINESS DATA ONLY' in api_prompts[0]
    ok('Saved API transport receives the same product and metrics (provider fixture)')
    assert not errors,errors
    ok('No JavaScript runtime errors in changed journeys')
    browser.close()
print(json.dumps({'checks':checks,'external_services':'fixtures only; not live homologation'},ensure_ascii=False))
