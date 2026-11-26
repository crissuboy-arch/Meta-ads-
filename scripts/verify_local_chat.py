"""Browser contract test with mocked native IPC; real CLI separately tested."""
import json
import os
import uuid
from playwright.sync_api import sync_playwright

base=os.environ.get('REDESIGN_TEST_URL','http://127.0.0.1:8824')
assert base.startswith(('http://127.0.0.1:','http://localhost:'))
with sync_playwright() as p:
    options={'headless':True}
    if os.environ.get('BROWSER_EXE'):options['executable_path']=os.environ['BROWSER_EXE']
    browser=p.chromium.launch(**options)
    page=browser.new_page()
    page.add_init_script('''localStorage.setItem('metaAdsLang','pt');
      window.nativeCalls=[];
      window.__TAURI__={core:{invoke:async(name,args)=>{
        if(name==='start_local_engine')return 43999;
        if(name==='detect_providers')return {claude:true,codex:true,opencode:false};
        if(name==='local_chat'){window.nativeCalls.push(args.payload);return {ok:true,text:'Resposta de teste de contrato'};}
        return null;
      }}};''')
    page.route('**/api/ads/live?**',lambda route:route.fulfill(json={'accounts':[],'preset':'today'}))
    page.route('**/api/chat',lambda route:route.abort())
    page.goto(base,wait_until='networkidle')
    page.locator('#authSwitchBtn').click()
    page.locator('#authEmail').fill('local-bridge-'+uuid.uuid4().hex[:8]+'@example.test')
    page.locator('#authPassword').fill('Isolated-validation-only-2026!')
    page.locator('#authSubmit').click()
    page.locator('#authOverlay.hidden').wait_for(state='attached')
    page.locator('#sideNav [data-id="mode"]').click()
    page.locator('[data-use-local="claude"]').click()
    page.locator('#sideNav [data-id="agents"]').click()
    ids=page.locator('[data-agent-chat]').evaluate_all('(items)=>items.map(x=>x.dataset.agentChat)')
    assert len(ids)==9
    for index,agent in enumerate(ids):
        page.locator('[data-agent-chat="'+agent+'"]').click()
        page.wait_for_function('(n)=>window.nativeCalls.length===n',arg=index+1)
        page.wait_for_function('()=>!busy')
        assert page.locator('.app.chat-expanded').count()==1
    calls=page.evaluate('window.nativeCalls')
    assert [c['module'] for c in calls]==ids
    assert all(c['provider']=='claude' and c['context']['read_only'] for c in calls)
    page.locator('#sideNav [data-id="mode"]').click()
    page.locator('[data-use-hosted]').click()
    assert page.evaluate('localStorage.getItem("ofensivaLocalProvider")') is None
    print(json.dumps({'specialists':9,'native_chat_routing':'passed','hosted_fallback_on_error':'disabled','real_cli':'tested separately'}))
    browser.close()
