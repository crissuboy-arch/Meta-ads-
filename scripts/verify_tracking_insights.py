"""Focused localhost browser checks. Webhook rows are explicit test fixtures only."""
import json
import time
import uuid
from pathlib import Path
from playwright.sync_api import sync_playwright

base='http://127.0.0.1:8831'
out=Path(__file__).resolve().parents[3]/'outputs/rastreamento-20261128'
out.mkdir(parents=True,exist_ok=True)
checks=[]
def passed(label):
    checks.append(label);print('PASS: '+label,flush=True)

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
    context=browser.new_context(viewport={'width':1512,'height':1200},service_workers='block',accept_downloads=True)
    page=context.new_page();errors=[];writes=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:writes.append(r.url) if r.method!='GET' and ('/api/ads/' in r.url or '/api/webhooks/' in r.url) else None)
    page.add_init_script("localStorage.setItem('metaAdsLang','pt')")
    page.goto(base,wait_until='networkidle')
    assert page.request.post(base+'/api/auth/register',data={'email':'tracking-'+uuid.uuid4().hex[:10]+'@ofensiva.test','password':'Local-Tracking-2026!'}).status==200
    page.reload(wait_until='networkidle');page.locator('#authOverlay.hidden').wait_for(state='attached')
    now=int(time.time());phase={'value':'normal'}
    rows=[
        {'id':'TESTE-1','ts':now,'status':'paid','amount':97,'currency':'BRL','utm_source':'facebook','utm_campaign':'Campanha A','capi_event':'Purchase','capi_status':'sent','capi_event_id':'TESTE-1'},
        {'id':'TESTE-2','ts':now-100,'status':'paid','amount':20,'currency':'USD','utm_source':'google','utm_campaign':'Campanha B','capi_status':'error:fixture'},
        {'id':'TESTE-3','ts':now-200,'status':'paid','amount':50,'currency':'BRL','utm_source':'facebook','capi_status':'no_credentials'},
        {'id':'TESTE-4','ts':now-300,'status':'pending','amount':1000,'currency':'BRL','utm_campaign':'<img src=x onerror=alert(1)>'},
    ]
    def sales(route):
        if phase['value']=='error':route.fulfill(status=503,json={'error':'fixture unavailable'})
        elif phase['value']=='limited':route.fulfill(json={'sales':[{**rows[0],'id':'TESTE-LIMIT-'+str(i)} for i in range(200)],'total':500})
        else:route.fulfill(json={'sales':rows if phase['value']=='normal' else [],'total':len(rows) if phase['value']=='normal' else 0})
    page.route('**/api/sales**',sales)
    page.locator('#sideNav [data-id="rastreamento"]').click()
    page.locator('#tiGroups table').wait_for()
    assert '147' in page.locator('#tiSummary').inner_text() and '20' in page.locator('#tiSummary').inner_text()
    assert 'Deduplicação: não comprovada' in page.locator('#tiDiagnostics').inner_text()
    assert page.locator('#trackingInsights img').count()==0
    passed('Real local authentication; webhook fixture statistics separate currencies and escape external labels')
    page.locator('[data-ti-diagnose="partial"]').click()
    assert page.locator('#tiEvents tbody tr').count()==1
    assert '50' in page.locator('#tiEvents').inner_text()
    page.locator('#tiCoverage').select_option('')
    page.locator('#tiCurrency').select_option('BRL')
    page.locator('#tiStatus').select_option('paid')
    page.locator('#tiQuery').fill('Campanha A')
    assert page.locator('#tiEvents tbody tr').count()==1
    passed('Combined period/state/currency/search filters and missing-UTM investigation')
    with page.expect_download() as download:page.locator('#tiExport').click()
    exported=Path(download.value.path()).read_text(encoding='utf-8-sig')
    assert 'TESTE-1' in exported and 'TESTE-2' not in exported
    passed('CSV download contains only filtered webhook records')
    page.locator('#tiQuery').fill('');page.locator('#tiCurrency').select_option('');page.locator('#tiStatus').select_option('')
    page.locator('#tiGroup').select_option('utm_source')
    assert 'facebook' in page.locator('#tiGroups').inner_text()
    page.locator('#tiEvents details').first.locator('summary').click()
    assert page.locator('#tiEvents').get_by_text('event_id do servidor',exact=True).count()>0
    passed('Source grouping and traceable event IDs remain available')
    page.locator('.ti-link-builder > summary').click()
    page.locator('#tiLink-url').fill('https://example.com/produto?coupon=REAL#checkout')
    page.locator('#tiLink-utm_source').fill('facebook')
    page.locator('#tiLink-utm_campaign').fill('Campanha São Paulo')
    page.locator('#tiLinkForm [type="submit"]').click()
    link=page.locator('#tiLinkResult').inner_text()
    assert 'coupon=REAL' in link and '#checkout' in link and 'utm_campaign=' in link
    assert page.locator('#tiCopyLink').is_enabled()
    page.locator('#tiLink-utm_campaign').fill('Outra campanha')
    assert page.locator('#tiCopyLink').is_disabled()
    passed('Tracked link generator preserves checkout parameters and invalidates outdated copied links')
    page.evaluate("document.body.insertAdjacentHTML('beforeend','<div style=\"position:fixed;top:8px;right:8px;z-index:99999;background:#28364b;color:white;padding:8px;font:12px Arial\">DADOS DE TESTE · NÃO SÃO VENDAS REAIS</div>')")
    page.evaluate("document.querySelectorAll('#trackingInsights details').forEach(el=>el.open=false);document.getElementById('trackingInsights').scrollIntoView({block:'start'})")
    page.screenshot(path=str(out/'01-rastreamento-desktop-fixture.png'))
    page.set_viewport_size({'width':390,'height':1050})
    page.evaluate("document.getElementById('trackingInsights').scrollIntoView({block:'start'})")
    assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1')
    page.screenshot(path=str(out/'02-rastreamento-mobile-fixture.png'))
    passed('Desktop and mobile layout without horizontal page overflow')
    phase['value']='error';page.locator('#tiRefresh').click()
    page.wait_for_function("document.getElementById('tiFeedback').classList.contains('error')")
    assert page.locator('#tiSummary').inner_text()=='' and page.locator('#tiExport').is_disabled()
    assert 'não interpretamos falhas' in page.locator('#tiFeedback').inner_text()
    phase['value']='empty';page.locator('#tiRefresh').click()
    page.wait_for_function("document.getElementById('tiFeedback').textContent.includes('Nenhum evento recebido')")
    passed('Integration failure and true absence of events produce distinct, honest states')
    phase['value']='limited';page.locator('#tiRefresh').click()
    page.wait_for_function("document.getElementById('tiFeedback').textContent.includes('histórico pode estar incompleto')")
    passed('A capped response is explicitly labeled as partial history')
    assert not errors,errors
    assert not writes,writes
    passed('No JavaScript errors, payment actions or Meta campaign writes')
    browser.close()
report={'checks':checks,'external_rows':'test fixtures only','live_account_validated':False,'production_modified':False}
(out/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
