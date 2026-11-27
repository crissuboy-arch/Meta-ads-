"""Targeted localhost UX tests. IPC/API fixtures are contracts, not live approvals."""
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE=os.environ.get('UX_PREVIEW_URL','http://127.0.0.1:8831')
assert BASE.startswith('http://127.0.0.1:')
OUT=Path(os.environ.get('UX_PREVIEW_OUTPUT','work/ux-validation'))
OUT.mkdir(parents=True,exist_ok=True)
checks=[]
errors=[]

def login(page):
    page.goto(BASE,wait_until='networkidle')
    page.locator('#authEmail').fill('previa@ofensiva.test')
    page.locator('#authPassword').fill('Previa-Local-2026!')
    page.locator('#authSubmit').click()
    page.locator('#authOverlay.hidden').wait_for(state='attached')

def nav(page,id):
    if page.locator('#mobileMenu').is_visible() and not page.locator('.side').is_visible():
        page.locator('#mobileMenu').click()
    page.locator('#sideNav [data-id="'+id+'"]').click()

with sync_playwright() as p:
    options={'headless':True}
    if os.environ.get('BROWSER_EXE'):options['executable_path']=os.environ['BROWSER_EXE']
    browser=p.chromium.launch(**options)
    page=browser.new_page(viewport={'width':1512,'height':1050},service_workers='block')
    page.add_init_script("localStorage.setItem('metaAdsLang','pt')")
    page.on('pageerror',lambda e:errors.append(str(e)))
    login(page)
    assert page.locator('[data-metric]').count()==12
    assert page.locator('[data-metric="net"] b').inner_text()=='—'
    page.screenshot(path=str(OUT/'01-dashboard.png'))
    checks.append('Existing authentication and twelve real-data/empty metric fields preserved')
    nav(page,'provedores')
    page.locator('[data-ux-connect="codex"]').wait_for()
    assert page.locator('[data-ux-provider]').count()==6
    assert page.locator('.cx-provider-logo img').count()==5
    assert page.locator('[data-ux-connect="opencode"]').is_disabled()
    assert 'Conexão testada' not in page.locator('#uxProviderRows').inner_text()
    page.screenshot(path=str(OUT/'02-central-ia.png'))
    page.locator('[data-ux-connect="codex"]').click()
    assert 'aplicativo Windows' in page.locator('#uxDialog').inner_text()
    assert page.locator('#uxDialog a').get_attribute('href').startswith('https://developers.openai.com/')
    page.locator('#uxDialog .cx-dialog-close').click()
    checks.append('Six provider actions, five official icons, honest web/experimental states')
    for provider in ['gemini','openrouter','own']:
        page.locator('[data-ux-connect="'+provider+'"]').click()
        assert page.locator('#uxApiDialog').is_visible()
        assert page.locator('#uxApiDialog [data-p="key"]').count()==4
        if provider!='own':
            assert page.locator('#uxApiDialog .prov-row:visible').count()==1
            assert page.locator('#uxApiDialog .prov-row:visible [data-p="prov"]').input_value()==provider
            page.locator('#uxApiDialog .prov-row:visible [data-pv="save"]').click()
            assert 'Informe a chave' in page.locator('#uxApiDialog .prov-row:visible [data-pvmsg]').inner_text()
        page.locator('#uxApiDialog .cx-dialog-close').click()
    checks.append('Provider-specific editor, all four existing slots, missing-key validation')
    page.locator('#provBody [data-ux-guide]').click()
    assert page.locator('#uxDialog [data-ux-step]').count()==9
    page.screenshot(path=str(OUT/'03-primeiro-acesso.png'))
    page.locator('[data-ux-step="2"]').click()
    page.locator('#uxProviderRows').wait_for()
    page.locator('#provBody [data-ux-guide]').click()
    assert '1 de 9 etapas visitadas' in page.locator('#uxDialog').inner_text()
    assert 'compra não verificada' in page.locator('#uxDialog').inner_text()
    page.locator('[data-ux-later]').click()
    checks.append('Nine-step guide, per-account local progress, no fictional purchase validation')
    nav(page,'agents')
    assert page.locator('[data-agent-chat]').count()==9
    assert page.locator('.ops-row').count()==9
    page.locator('.ops-row[data-ux-agent="3"] h3').click()
    assert 'Auditor de Campanhas' in page.locator('#uxAgentBrief').inner_text()
    page.screenshot(path=str(OUT/'04-central-agentes.png'))
    checks.append('Nine existing specialists, selectable context panel, provider chooser')
    for width in [1512,1024,768,390,360]:
        page.set_viewport_size({'width':width,'height':950})
        assert page.evaluate('document.documentElement.scrollWidth')<=width
        nav(page,'provedores')
        page.locator('[data-ux-connect="claude"]').wait_for(state='visible')
        assert page.evaluate('document.documentElement.scrollWidth')<=width
        if width==390:page.screenshot(path=str(OUT/'05-mobile.png'))
    checks.append('Five resolutions: no horizontal overflow, reachable actions')
    page.set_viewport_size({'width':1512,'height':1050})
    # API transport fixtures: no credential or record leaves this browser.
    saved=[{'id':'fixture-primary','provider':'openrouter','kind':'text','role':'primary','has_key':True,'last_test_ok':True,'key_hint':'test-only','model':'fixture-model'}]
    saved.append({'id':'fixture-backup','provider':'anthropic','kind':'text','role':'backup','has_key':True,'last_test_ok':True,'key_hint':'test-only','model':'fixture-model'})
    page.route('**/api/providers',lambda route:route.fulfill(json={'providers':saved}))
    generated=[]
    def generation(route):
        generated.append(route.request.post_data_json)
        route.fulfill(json={'ok':True,'text':'Resposta de contrato de API.','provider':'openrouter'})
    page.route('**/api/providers/generate',generation)
    nav(page,'provedores')
    page.locator('[data-ux-use-api]').click()
    page.locator('#uxDialog .cx-dialog-close').click()
    nav(page,'agents')
    page.locator('[data-agent-chat]').first.click()
    page.wait_for_function("document.querySelector('#sendBtn').disabled===false")
    assert len(generated)==1 and generated[0]['kind']=='text'
    assert 'read_only' in generated[0]['prompt']
    assert 'Resposta de contrato de API.' in page.locator('#log').inner_text()
    checks.append('Saved BYOK profile reaches existing generation endpoint with read-only account context')
    if page.locator('#chatClose').is_visible():page.locator('#chatClose').click()
    nav(page,'provedores')
    page.locator('[data-ux-disconnect="own"]').wait_for()
    assert 'Último teste aprovado' in page.locator('[data-ux-provider="own"]').inner_text()
    def disconnect_fixture(route):
        saved[:]=[row for row in saved if row['id']!='fixture-backup']
        route.fulfill(json={'ok':True})
    page.route('**/api/providers/fixture-backup',disconnect_fixture)
    page.locator('[data-ux-disconnect="own"]').click()
    page.locator('[data-ux-confirm-disconnect]').click()
    page.locator('#uxDialog .cx-dialog-close').click()
    page.wait_for_function("document.querySelector('[data-ux-provider=own] .cx-state').dataset.state==='idle'")
    assert len(saved)==1 and saved[0]['provider']=='openrouter'
    checks.append('Legacy Anthropic connection is visible; API disconnect preserves other providers')
    page.close()
    native=browser.new_page(viewport={'width':1512,'height':1050},service_workers='block')
    native.on('pageerror',lambda e:errors.append(str(e)))
    native.add_init_script('''localStorage.setItem('metaAdsLang','pt');window.uxNativeCalls=[];window.uxNativeFail=false;
      window.__TAURI__={core:{invoke:async(name,args)=>{
        window.uxNativeCalls.push({name,args});
        if(name==='detect_providers')return {codex:true,claude:true,opencode:true};
        if(name==='local_chat')return window.uxNativeFail?{ok:false,error:'login_required'}:{ok:true,text:'Resposta de contrato nativo.'};
        if(name==='start_local_engine')return 43999;
        return null;
      }}};''')
    native.route('**/api/chat',lambda route:route.abort())
    login(native)
    nav(native,'provedores')
    assert 'Conexão testada' not in native.locator('#uxProviderRows').inner_text()
    native.locator('[data-ux-connect="claude"]').click()
    native.locator('[data-ux-login]').click()
    assert 'Conexão testada' not in native.locator('[data-ux-provider="claude"]').inner_text()
    native.locator('[data-ux-native-test]').click()
    native.locator('[data-ux-provider="claude"] .cx-state[data-state="verified"]').wait_for()
    native.locator('#uxDialog .cx-dialog-close').click()
    nav(native,'agents')
    for index in range(9):
        if native.locator('#chatClose').is_visible():native.locator('#chatClose').click()
        native.locator('[data-agent-chat]').nth(index).click()
        native.wait_for_function("document.querySelector('#sendBtn').disabled===false")
    calls=native.evaluate('window.uxNativeCalls')
    chats=[c['args']['payload'] for c in calls if c['name']=='local_chat']
    assert len(chats)==10 and all(c['provider']=='claude' for c in chats)
    assert len({c['module'] for c in chats[1:]})==9
    assert all(c['context']['read_only'] is True for c in chats)
    assert any(c['name']=='open_provider_terminal' for c in calls)
    checks.append('Mocked native contract: official flow dispatch, real-response gate, nine agent routes and no hosted fallback')
    if native.locator('#chatClose').is_visible():native.locator('#chatClose').click()
    nav(native,'provedores')
    native.evaluate('window.uxNativeFail=true')
    native.locator('[data-ux-test="claude"]').click()
    native.locator('[data-ux-test-now]').click()
    native.locator('[data-ux-provider="claude"] .cx-state[data-state="error"]').wait_for()
    assert native.locator('#uxDialog [data-ux-feedback][data-error="true"]').is_visible()
    native.locator('#uxDialog .cx-dialog-close').click()
    native.locator('[data-ux-disconnect="claude"]').click()
    assert native.evaluate('localStorage.getItem("ofensivaLocalProvider")') is None
    checks.append('Native failure is not connected; disconnect removes only app selection')
    native.locator('#uxDialog .cx-dialog-close').click()
    native.evaluate("localStorage.setItem('ofensivaLocalProvider','opencode')")
    nav(native,'agents')
    assert native.locator('#uxAgentProvider').input_value()=='opencode'
    assert 'experimental' in native.locator('#uxAgentProvider option:checked').inner_text()
    checks.append('Pre-existing experimental OpenCode selection is preserved without claiming approval')
    native.close()
    assert not errors,errors
    report={'checks':checks,'count':len(checks),'javascript_errors':errors,
            'native_tests':'mocked IPC contracts; no new live authentication or inference',
            'api_tests':'browser-only fixtures; no real credentials',
            'screenshots':'real local empty states, no fictitious metrics',
            'production_changed':False}
    (OUT/'validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True,indent=2))
    browser.close()
