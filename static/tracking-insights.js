/* Tracking insights: existing webhook records only. No requests to payment or Meta APIs. */
const TrackingInsights = (() => {
  const utms = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'];
  const text = value => String(value ?? '').trim();
  const amount = row => ['number','string'].includes(typeof row.amount) && text(row.amount) !== '' && Number.isFinite(Number(row.amount)) && Number(row.amount) >= 0 ? Number(row.amount) : null;
  const currency = row => /^[A-Z]{3}$/.test(text(row.currency).toUpperCase()) ? text(row.currency).toUpperCase() : 'UNKNOWN';
  function coverage(row) {
    if (text(row.utm_source) && text(row.utm_campaign)) return 'complete';
    return utms.some(key => text(row[key])) ? 'partial' : 'missing';
  }
  function unique(rows) {
    const seen = new Map(), result = [];
    // Only exact event IDs are collapsed. Do not infer a shared transaction from similar amounts.
    for (const row of rows.filter(row => row && typeof row === 'object' && !Array.isArray(row)).sort((a,b) => Number(b.ts || 0) - Number(a.ts || 0))) {
      const key = text(row.id);
      if (key && seen.has(key)) continue;
      if (key) seen.set(key,true);
      result.push(row);
    }
    return result;
  }
  function filter(rows, options = {}) {
    return unique(rows).filter(row => {
      const ts = Number(row.ts);
      if (options.since != null && (!Number.isFinite(ts) || ts < options.since)) return false;
      if (options.until != null && (!Number.isFinite(ts) || ts >= options.until)) return false;
      for (const field of ['status','method']) if (options[field] && row[field] !== options[field]) return false;
      if (options.currency && currency(row) !== options.currency) return false;
      if (options.coverage && coverage(row) !== options.coverage) return false;
      if (options.query) {
        const haystack = [row.id,row.platform,...utms.map(key => row[key])].join(' ').toLocaleLowerCase();
        if (!haystack.includes(text(options.query).toLocaleLowerCase())) return false;
      }
      return true;
    });
  }
  function summarize(rows, groupBy = 'utm_campaign') {
    if (![...utms,'platform','method'].includes(groupBy)) throw new Error('Agrupamento inválido.');
    const paid = rows.filter(row => row.status === 'paid'), totals = {}, groups = new Map();
    for (const row of rows) {
      const cur = currency(row), value = amount(row);
      const total = totals[cur] ||= {paid:0,revenue:cur==='UNKNOWN'?null:0,unknownAmount:0,pending:0,refunded:0};
      if (row.status === 'paid') { total.paid++; if (value === null) total.unknownAmount++; else if(cur!=='UNKNOWN') total.revenue += value; }
      if (row.status === 'pending') total.pending++;
      if (row.status === 'refunded') total.refunded++;
      const label = text(row[groupBy]) || 'Não informado';
      const key = JSON.stringify([label,cur]);
      const group = groups.get(key) || {label,currency:cur,records:0,paid:0,revenue:cur==='UNKNOWN'?null:0,unknownAmount:0};
      group.records++;
      if (row.status === 'paid') { group.paid++; if (value === null) group.unknownAmount++; else if(cur!=='UNKNOWN') group.revenue += value; }
      groups.set(key,group);
    }
    const complete = paid.filter(row => coverage(row) === 'complete').length;
    return {totals,groups:[...groups.values()].sort((a,b) => b.paid-a.paid || a.label.localeCompare(b.label)),
      paid:paid.length,complete,partial:paid.filter(row => coverage(row) === 'partial').length,
      missing:paid.filter(row => coverage(row) === 'missing').length,
      coverage:paid.length ? complete/paid.length*100 : null,
      capiAccepted:paid.filter(row => row.capi_event === 'Purchase' && row.capi_status === 'sent').length,
      capiErrors:paid.filter(row => text(row.capi_status).startsWith('error:')).length,
      capiMissingCredentials:paid.filter(row => row.capi_status === 'no_credentials').length,
      missingEventId:paid.filter(row => !text(row.capi_event_id)).length};
  }
  function trackedUrl(base, values) {
    const url = new URL(base);
    if (!['http:','https:'].includes(url.protocol) || url.username || url.password) throw new Error('Use um endereço HTTP ou HTTPS sem credenciais.');
    if (!text(values.utm_source) || !text(values.utm_campaign)) throw new Error('Informe a origem e o nome da campanha.');
    for (const key of utms) {
      const value = text(values[key]);
      if (value.length > 250) throw new Error('Cada parâmetro deve ter no máximo 250 caracteres.');
      if (value) url.searchParams.set(key,value); else url.searchParams.delete(key);
    }
    return url.toString();
  }
  function csv(rows) {
    const columns = ['id','ts','platform','status','method','currency','amount',...utms,'capi_event','capi_status','capi_event_id'];
    function cell(value) {
      let s = String(value ?? '');
      // Prevent spreadsheet formulas, including formulas preceded by whitespace/control characters.
      if (/^[\s\u0000-\u001f]*[=+@-]/.test(s)) s = "'" + s;
      return '"' + s.replace(/"/g,'""') + '"';
    }
    const value=(row,key)=>key==='capi_status' ? (text(row[key]).startsWith('error:')?'error':['sent','no_credentials','skipped'].includes(row[key])?row[key]:'unknown') : row[key];
    return '\uFEFF' + [columns.map(cell).join(';'),...rows.map(row => columns.map(key => cell(value(row,key))).join(';'))].join('\r\n');
  }
  return {utms,amount,currency,coverage,unique,filter,summarize,trackedUrl,csv};
})();
if (typeof module !== 'undefined' && module.exports) module.exports = TrackingInsights;

if (typeof document !== 'undefined') (() => {
  const state = {rows:[],key:'',sequence:0,status:'idle',error:'',updated:null,filtered:[],limited:false};
  const esc = value => trkEsc(String(value ?? ''));
  function money(value,cur) {
    if(value===null)return 'Não apurável';
    if (cur === 'UNKNOWN') return Number(value).toLocaleString(lvLoc()) + ' · moeda não informada';
    try { return Number(value).toLocaleString(lvLoc(),{style:'currency',currency:cur}); }
    catch { return Number(value).toLocaleString(lvLoc()) + ' ' + cur; }
  }
  const capiLabel = row => row.capi_status === 'sent' ? 'Aceito pela API' : String(row.capi_status || '').startsWith('error:') ? 'Falha no envio' : row.capi_status === 'no_credentials' ? 'Credenciais ausentes' : 'Envio não confirmado';
  const statusLabel = row => ({paid:'Pagamento informado',pending:'Pendente',refunded:'Reembolso registrado'})[row.status] || 'Estado não informado';
  function ensure() {
    let root = document.getElementById('trackingInsights');
    if (root) return root;
    root = document.createElement('div');root.id='trackingInsights';root.className='ti-workspace';
    document.getElementById('trkProdBar').after(root);
    root.innerHTML = '<div class="page-heading"><div><span class="eyebrow">RASTREAMENTO & ATRIBUIÇÃO</span><h2>Saiba de onde vêm suas vendas.</h2><p>Leia os registros recebidos, encontre falhas de identificação e acompanhe os envios ao Meta.</p></div><button class="btn-s" type="button" id="tiRefresh">Atualizar registros</button></div>'+
      '<p class="metric-note" id="tiProductContext"></p><div class="ti-toolbar"><label>Período<select class="url-input" id="tiPeriod"><option value="7">Últimos 7 dias</option><option value="today">Hoje</option><option value="30">Últimos 30 dias</option><option value="all">Todos os registros carregados</option></select></label><label>Moeda<select class="url-input" id="tiCurrency"><option value="">Todas, separadamente</option></select></label><label>Estado<select class="url-input" id="tiStatus"><option value="">Todos</option><option value="paid">Pagamento informado</option><option value="pending">Pendente</option><option value="refunded">Reembolso registrado</option></select></label><label>Identificação<select class="url-input" id="tiCoverage"><option value="">Todas</option><option value="complete">Origem e campanha presentes</option><option value="partial">UTMs incompletas</option><option value="missing">UTMs ausentes</option></select></label><label>Procurar<input class="url-input" type="search" id="tiQuery" placeholder="Campanha, origem ou evento"></label></div>'+
      '<div id="tiFeedback" class="metrics-state" role="status" aria-live="polite"></div><div id="tiSummary" class="ti-summary"></div><div id="tiDiagnostics" class="ti-diagnostics"></div>'+
      '<div class="ti-section"><div class="metrics-toolbar"><h3>Desempenho por identificação</h3><label>Agrupar por <select class="url-input" id="tiGroup"><option value="utm_campaign">Campanha</option><option value="utm_source">Origem</option><option value="utm_content">Anúncio / criativo</option><option value="utm_term">Público / conjunto</option><option value="platform">Plataforma de venda</option><option value="method">Forma de pagamento</option></select></label></div><div id="tiGroups" class="ti-table-wrap"></div></div>'+
      '<div class="ti-section"><div class="metrics-toolbar"><div><h3>Eventos recebidos</h3><p class="metric-note">A data é a do recebimento pelo sistema; não confirma a data bancária da transação.</p></div><button class="btn-s" type="button" id="tiExport">Exportar CSV filtrado</button></div><div id="tiEvents" class="ti-table-wrap"></div></div>'+
      '<details class="ti-link-builder"><summary>Criar um link rastreado para meu anúncio</summary><form id="tiLinkForm"><p class="metric-note">Gere o link e cole no anúncio. Não alteramos campanhas. O checkout precisa preservar as UTMs para que elas retornem no webhook.</p><div class="utm-grid">'+
      [['url','Página de destino','https://seusite.com/produto'],['utm_source','Origem','facebook, instagram, google…'],['utm_medium','Tipo de tráfego','paid_social, email…'],['utm_campaign','Nome da campanha','Nome usado por você'],['utm_term','Público / conjunto (opcional)','Identifique o público'],['utm_content','Anúncio / criativo (opcional)','Identifique a versão']].map(([key,label,ph])=>'<label>'+label+'<input class="url-input" id="tiLink-'+key+'" '+(key==='url'?'type="url"':'type="text"')+' placeholder="'+ph+'"'+(['url','utm_source','utm_campaign'].includes(key)?' required':'')+'></label>').join('')+
      '</div><div class="cx-actions"><button class="btn-p" type="submit">Gerar link</button><button class="btn-s" id="tiCopyLink" type="button" disabled>Copiar link</button></div><output id="tiLinkResult" class="utm-result" style="display:block;overflow-wrap:anywhere"></output><p id="tiLinkMessage" class="cx-feedback" role="status"></p></form></details>'+
      '<p class="metric-note ti-scope">Fonte: webhooks já recebidos pelo produto selecionado. Até 200 registros por consulta; os totais representam somente a amostra carregada. Não misturamos moedas nem tratamos atribuição como saldo bancário. Não calculamos ROAS sem conciliação de campanhas e período.</p>';
    for (const id of ['tiPeriod','tiCurrency','tiStatus','tiCoverage','tiGroup']) root.querySelector('#'+id).onchange=render;
    root.querySelector('#tiQuery').oninput=render;
    root.querySelector('#tiRefresh').onclick=()=>load(true);
    root.querySelector('#tiExport').onclick=()=>{
      if (state.status!=='ready'||state.key!==trkKey()||!state.filtered.length) return;
      const url=URL.createObjectURL(new Blob([TrackingInsights.csv(state.filtered)],{type:'text/csv;charset=utf-8'}));
      const a=document.createElement('a');a.href=url;a.download='ofensiva-eventos-'+new Date().toISOString().slice(0,10)+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    };
    root.querySelector('#tiLinkForm').onsubmit=e=>{e.preventDefault();const msg=root.querySelector('#tiLinkMessage');try{const values={};for(const key of TrackingInsights.utms)values[key]=root.querySelector('#tiLink-'+key).value;const url=TrackingInsights.trackedUrl(root.querySelector('#tiLink-url').value,values);root.querySelector('#tiLinkResult').textContent=url;root.querySelector('#tiCopyLink').disabled=false;msg.textContent='Link gerado. Valide o repasse de parâmetros no checkout antes de anunciar.'}catch(error){root.querySelector('#tiCopyLink').disabled=true;root.querySelector('#tiLinkResult').textContent='';msg.textContent=error.message}};
    root.querySelector('#tiCopyLink').onclick=async()=>{const msg=root.querySelector('#tiLinkMessage');try{await navigator.clipboard.writeText(root.querySelector('#tiLinkResult').textContent);msg.textContent='Link copiado.'}catch{msg.textContent='Não foi possível copiar automaticamente. Selecione e copie o link acima.'}};
    root.querySelector('#tiLinkForm').oninput=()=>{root.querySelector('#tiLinkResult').textContent='';root.querySelector('#tiCopyLink').disabled=true};
    return root;
  }
  function options() {
    const value=id=>document.getElementById(id).value;
    const opt={currency:value('tiCurrency'),status:value('tiStatus'),coverage:value('tiCoverage'),query:value('tiQuery')};
    const period=value('tiPeriod');
    if(period!=='all') {const start=new Date();start.setHours(0,0,0,0);if(period!=='today')start.setDate(start.getDate()-Number(period)+1);opt.since=start.getTime()/1000;const end=new Date();end.setHours(24,0,0,0);opt.until=end.getTime()/1000;}
    return opt;
  }
  function render() {
    const root=ensure(), feedback=root.querySelector('#tiFeedback');
    const unavailable=state.status!=='ready'||state.key!==trkKey();
    root.querySelector('#tiRefresh').disabled=state.status==='loading';
    if(unavailable){state.filtered=[];for(const id of ['tiSummary','tiDiagnostics','tiGroups','tiEvents'])root.querySelector('#'+id).replaceChildren();root.querySelector('#tiExport').disabled=true;feedback.textContent=state.status==='error'?state.error:'Carregando os registros deste produto…';feedback.className='metrics-state'+(state.status==='error'?' error':'');return;}
    const rows=TrackingInsights.filter(state.rows,options()), data=TrackingInsights.summarize(rows,root.querySelector('#tiGroup').value);state.filtered=rows;
    root.querySelector('#tiExport').disabled=!rows.length;
    const time=state.updated.toLocaleTimeString(lvLoc()),zone=Intl.DateTimeFormat().resolvedOptions().timeZone;
    feedback.className='metrics-state';feedback.textContent=!state.rows.length?'Nenhum evento recebido para este produto. Confira o webhook e siga o assistente de instalação abaixo.':!rows.length?'Nenhum registro corresponde aos filtros. Ajuste o período ou a busca.':rows.length+' registros no filtro · atualizado às '+time+' · fuso '+zone+(state.limited?' · limite da consulta atingido; o histórico pode estar incompleto.':'.');
    const totals=Object.entries(data.totals).map(([cur,total])=>'<strong>'+esc(total.paid>0&&total.unknownAmount===total.paid?'Valor não informado':money(total.revenue,cur))+'</strong><small>'+total.paid+' pagamentos informados'+(total.unknownAmount?' · '+total.unknownAmount+' sem valor válido':'')+'</small>').join('')||'<strong>—</strong><small>Sem pagamentos no filtro</small>';
    root.querySelector('#tiSummary').innerHTML='<div><span>Receita paga informada</span>'+totals+'</div><div><span>Origem + campanha presentes</span><strong>'+(data.coverage==null?'—':data.coverage.toFixed(1)+'%')+'</strong><small>'+data.complete+' de '+data.paid+' pagamentos informados</small></div><div><span>Purchase aceitos pela API</span><strong>'+data.capiAccepted+'</strong><small>Recebimento pelo Meta não confirma atribuição</small></div>';
    root.querySelector('#tiDiagnostics').innerHTML='<h3>O que precisa de atenção</h3><div class="ti-diagnostic-grid">'+[
      [data.missing+' sem UTMs','Revise o link do anúncio e o repasse de parâmetros até o checkout.','missing'],
      [data.partial+' com UTMs incompletas','Origem e campanha juntas permitem identificar melhor a venda.','partial'],
      ['Falhas de CAPI: '+data.capiErrors+' · Sem credenciais: '+data.capiMissingCredentials,'Confira a configuração e use o teste autorizado abaixo.',''],
      ['Deduplicação: não comprovada aqui','É necessário comparar o mesmo event_id no navegador e no servidor. A presença do ID no webhook não comprova deduplicação.','']
    ].map(([title,description,filter])=>'<div><b>'+esc(title)+'</b><p>'+description+'</p>'+(filter?'<button type="button" class="cx-link" data-ti-diagnose="'+filter+'">Investigar registros →</button>':'')+'</div>').join('')+'</div>';
    root.querySelectorAll('[data-ti-diagnose]').forEach(b=>b.onclick=()=>{root.querySelector('#tiCoverage').value=b.dataset.tiDiagnose;root.querySelector('#tiStatus').value='paid';render()});
    root.querySelector('#tiGroups').innerHTML=!rows.length?'<p class="metric-note">Sem dados para agrupar.</p>':'<table class="trk-table"><thead><tr><th>Identificação recebida</th><th>Moeda</th><th>Registros</th><th>Pagamentos informados</th><th>Receita informada</th></tr></thead><tbody>'+data.groups.map(g=>'<tr><td>'+esc(g.label)+'</td><td>'+esc(g.currency==='UNKNOWN'?'Não informada':g.currency)+'</td><td>'+g.records+'</td><td>'+g.paid+'</td><td>'+esc(g.paid>0&&g.unknownAmount===g.paid?'Valor não informado':money(g.revenue,g.currency))+(g.unknownAmount?' · valores incompletos':'')+'</td></tr>').join('')+'</tbody></table>';
    root.querySelector('#tiEvents').innerHTML=!rows.length?'<p class="metric-note">Os eventos aparecerão aqui quando forem recebidos.</p>':'<table class="trk-table"><thead><tr><th>Recebido em</th><th>Estado</th><th>Valor informado</th><th>Origem / campanha</th><th>CAPI</th><th>Detalhes</th></tr></thead><tbody>'+rows.map(row=>{
      const date=Number(row.ts)>0?new Date(Number(row.ts)*1000).toLocaleString(lvLoc()):'Data não informada';
      const value=TrackingInsights.amount(row);
      return '<tr><td>'+esc(date)+'</td><td>'+esc(statusLabel(row))+'</td><td>'+esc(value===null?'Não informado':money(value,TrackingInsights.currency(row)))+'</td><td>'+esc(row.utm_source||'Origem ausente')+'<br><small>'+esc(row.utm_campaign||'Campanha ausente')+'</small></td><td>'+esc(capiLabel(row))+'</td><td><details><summary>Ver evento</summary><dl>'+[['ID do registro',row.id],['Evento CAPI',row.capi_event],['event_id do servidor',row.capi_event_id],['Plataforma',row.platform],...TrackingInsights.utms.map(key=>[key,row[key]])].map(([key,value])=>'<dt>'+esc(key)+'</dt><dd>'+esc(value||'Não informado')+'</dd>').join('')+'</dl></details></td></tr>';
    }).join('')+'</tbody></table>';
  }
  async function load(force=false) {
    const root=ensure(),key=trkKey();
    if(!force&&state.status==='loading'&&state.key===key)return;
    const currentProduct=trkProducts().find(p=>p.key===key);root.querySelector('#tiProductContext').textContent='Produto de rastreamento: '+(currentProduct?.name||'Selecionado acima')+'. Os filtros e os totais abaixo se referem a este produto.';state.key=key;state.status='loading';state.rows=[];const sequence=++state.sequence;render();
    try {
      const response=await fetch('/api/sales?key='+encodeURIComponent(key));
      if(!response.ok)throw new Error(response.status===401?'Entre na sua conta para consultar os eventos.':'Não foi possível consultar os registros. Tente atualizar; não interpretamos falhas como ausência de vendas.');
      const data=await response.json();if(!Array.isArray(data.sales))throw new Error('O servidor retornou registros em formato inesperado.');
      if(sequence!==state.sequence||key!==trkKey())return;
      state.rows=TrackingInsights.unique(data.sales);state.limited=data.sales.length>=200;state.status='ready';state.updated=new Date();
      const currencySelect=root.querySelector('#tiCurrency'),previous=currencySelect.value;
      currencySelect.innerHTML='<option value="">Todas, separadamente</option>'+[...new Set(state.rows.map(TrackingInsights.currency))].sort().map(cur=>'<option value="'+esc(cur)+'">'+esc(cur==='UNKNOWN'?'Moeda não informada':cur)+'</option>').join('');
      currencySelect.value=[...currencySelect.options].some(o=>o.value===previous)?previous:'';
      if(typeof BF!=='undefined'&&BF.product?.tracking_key===key){const input=root.querySelector('#tiLink-url');if(!input.value)input.value=BF.product.url||'';}
      render();
    } catch(error) {if(sequence!==state.sequence)return;state.status='error';state.error=error.message;render();}
  }
  const previousOpen=openTrackingScreen;
  openTrackingScreen=function(){previousOpen();load();};
  const previousSwitch=trkSwitchProduct;
  trkSwitchProduct=function(key){previousSwitch(key);load(true);};
  document.getElementById('trkSalesRefresh').addEventListener('click',()=>load(true));
})();
