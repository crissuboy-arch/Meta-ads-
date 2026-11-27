"""Browser regression checks against a LOCAL app; never uses production accounts.

Run the app with an isolated META_ADS_DATA_DIR and no external credentials.
Requires playwright and a browser (BROWSER_EXE may point to installed Edge).
Metric fixtures below exist only inside this test browser's intercepted responses.
"""
import json
import os
import uuid
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get('REDESIGN_TEST_URL', 'http://127.0.0.1:8812')
assert BASE.startswith(('http://127.0.0.1:', 'http://localhost:')), 'Local validation only'
OUT = Path(os.environ.get('REDESIGN_OUTPUT_DIR', 'work/ui-validation'))
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    options={'headless': True}
    if os.environ.get('BROWSER_EXE'): options['executable_path']=os.environ['BROWSER_EXE']
    browser=p.chromium.launch(**options)
    page=browser.new_page(viewport={'width':1512,'height':1100},service_workers='block')
    page.add_init_script("localStorage.setItem('metaAdsLang','pt')")
    errors=[]; checks=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(BASE,wait_until='networkidle')
    page.locator('#authOverlay:not(.hidden)').wait_for()
    assert page.locator('#authEmail').get_attribute('type')=='email'
    assert page.locator('#authPassword').get_attribute('minlength')=='8'
    page.locator('#authPwToggle').click()
    assert page.locator('#authPassword').get_attribute('type')=='text'
    page.locator('#authPwToggle').click()
    page.locator('#authThemeToggle').click()
    assert 'light' in page.locator('#authOverlay').get_attribute('class')
    page.locator('#authThemeToggle').click()
    page.screenshot(path=str(OUT/'01-login.png'))
    page.locator('#authSwitchBtn').click()
    email='redesign-'+uuid.uuid4().hex[:10]+'@example.test'
    page.locator('#authEmail').fill(email)
    page.locator('#authPassword').fill('Local-validation-only-2026!')
    with page.expect_response('**/api/auth/register') as response:page.locator('#authSubmit').click()
    assert response.value.status==200
    page.locator('#authOverlay.hidden').wait_for(state='attached')
    page.locator('#premiumOverview [data-metric="spend"]').wait_for()
    checks.append('Real local registration, password visibility, login theme')
    page.wait_for_timeout(400)
    page.screenshot(path=str(OUT/'02-dashboard.png'))

    views={'agents':'agentsSection','provedores':'provSection','finance':'financeSection','ads-connect':'adsSection','claude-connect':'claudeSection','mode':'modeSection','settings':'settingsSection','analysis':'workspaceSection','products':'workspaceSection','mentor':'workspaceSection','criar':'criarSection','campwiz':'campwizSection','biblioteca':'bibSection','rastreamento':'trackingSection','ads-live':'adsLiveSection'}
    captures={'agents':'03-equipa','provedores':'04-central-ia','finance':'05-financeiro','ads-connect':'06-meta-ads','mode':'07-modos','criar':'09-criativos','rastreamento':'10-rastreamento','campwiz':'11-campanhas'}
    def navigate(nav):
        page.locator(f'#sideNav [data-id="{nav}"]').click()
        page.wait_for_timeout(150)
    for nav,section in views.items():
        navigate(nav)
        assert page.locator('#'+section).is_visible(),nav
        assert not page.locator('#premiumOverview').is_visible(),nav
        # An async completion must not navigate back to the dashboard.
        page.wait_for_timeout(300)
        assert not page.locator('#premiumOverview').is_visible(),nav
        if nav=='agents':assert page.locator('[data-agent-chat]').count()==9
        if nav=='provedores':assert page.locator('[data-p="key"]').count()==4
        if nav in captures:page.screenshot(path=str(OUT/(captures[nav]+'.png')))
        checks.append('Navigation: '+nav)
    navigate('finance')
    page.locator('#finCalc').click()
    assert page.locator('#finMsg').inner_text()
    page.locator('#finPrice').fill('100')
    page.locator('#finSpend').fill('100')
    page.locator('#finPurchases').fill('3')
    with page.expect_response('**/api/finance/calc') as response:page.locator('#finCalc').click()
    assert response.value.status==200
    assert '200' in page.locator('#finResult').inner_text()
    checks.append('Finance invalid form and real API calculation')

    navigate('painel')
    page.locator('#chatToggle').click()
    assert page.locator('#chatPanel').is_visible()
    page.locator('#chatClose').click()
    assert not page.locator('#chatPanel').is_visible()
    checks.append('Collapsible chat')
    for width,height in [(1920,1080),(1366,768),(1024,768),(768,1024),(390,844),(360,800)]:
        page.set_viewport_size({'width':width,'height':height})
        assert page.evaluate('document.documentElement.scrollWidth')<=width,(width,'horizontal overflow')
        if width<900:
            page.locator('#mobileMenu').click()
            assert page.locator('.side').is_visible()
            navigate('agents')
            assert not page.locator('.side').is_visible()
            page.locator('#mobileMenu').click();navigate('painel')
        if width==390:page.screenshot(path=str(OUT/'08-mobile.png'))
        checks.append('Resolution: '+str(width)+'x'+str(height))
    page.set_viewport_size({'width':1512,'height':1100})

    # Browser-only fixtures verify arithmetic and missing/partial/mixed-currency states.
    # No fixture is saved into application data or used in delivery screenshots.
    account={'account_id':'fixture','name':'TEST FIXTURE','currency':'EUR','account_status':'ACTIVE','spend':100,'revenue':300,'purchases':3,'clicks':50,'impressions':1000,'reach':500,'frequency':2,'active_campaigns':2,'results':3,'result_type':'purchase'}
    data={'accounts':[account]}
    def fixture(route):route.fulfill(json=data)
    page.route('**/api/ads/live?**',fixture)
    page.locator('#premiumRefresh').click()
    page.wait_for_function("document.querySelector('[data-metric=roas] b').textContent.includes('3')")
    assert '200' not in page.locator('[data-metric="net"] b').inner_text()
    assert page.locator('[data-metric="net"] b').inner_text()=='—'
    assert page.locator('[data-metric="roi"] b').inner_text()=='—'
    assert page.locator('[data-metric="ctr"] b').inner_text()=='5%'
    checks.append('Metric formulas; no fabricated net profit or ROI')
    data['accounts']=[account,dict(account,account_id='usd',currency='USD',spend=900,revenue=1800)]
    page.locator('#premiumRefresh').click();page.locator('#premiumCurrency').wait_for()
    page.wait_for_timeout(150)
    assert page.locator('#premiumCurrency option').count()==2
    assert '100' in page.locator('[data-metric="spend"] b').inner_text()
    page.locator('#premiumCurrency').select_option('USD')
    assert '900' in page.locator('[data-metric="spend"] b').inner_text()
    checks.append('Currencies never combined')
    data['accounts']=[account,dict(account,account_id='broken',error='fixture failure')]
    page.locator('#premiumRefresh').click();page.wait_for_timeout(200)
    assert '1 conta(s) com falha' in page.locator('#premiumOverview .metrics-state').inner_text()
    checks.append('Partial integration failures')
    data['accounts']=[]
    page.locator('#premiumRefresh').click();page.wait_for_timeout(200)
    assert 'Ainda não há contas' in page.locator('#premiumOverview .metrics-state').inner_text()
    checks.append('Empty state')
    page.unroute('**/api/ads/live?**',fixture)
    page.locator('#logoutBtn').click()
    page.locator('#authOverlay:not(.hidden)').wait_for()
    page.locator('#authEmail').fill(email)
    page.locator('#authPassword').fill('wrong-password-for-validation')
    with page.expect_response('**/api/auth/login') as response:page.locator('#authSubmit').click()
    assert response.value.status==401
    page.locator('#authPassword').fill('Local-validation-only-2026!')
    with page.expect_response('**/api/auth/login') as response:page.locator('#authSubmit').click()
    assert response.value.status==200
    checks.append('Logout, invalid credentials and real local login')
    assert not errors,errors
    report={'checks':checks,'count':len(checks),'javascript_errors':errors,'external_live_connections':'not tested; no real credentials used','metric_fixtures':'test browser only; excluded from screenshots'}
    (OUT/'browser-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    browser.close()
