"""Owner-scoped business context. Existing storage/MCP; no schema or payment changes."""
import hashlib
import json
import math
import re
import secrets
import threading
from datetime import datetime, timezone

from fastapi import HTTPException, Request
from starlette.concurrency import run_in_threadpool
import finance

SLUG = '__business_workspace_v1'
LOCK = threading.RLock()
PRESETS = {'today','yesterday','last_7d','last_30d','this_month'}
COSTS = ('unit_cost','fee_pct','fee_fixed','tax_pct','other_costs','margin_pct')


def number(value, name, maximum=None):
    if value in (None, ''):
        return None
    if isinstance(value, bool):
        raise ValueError(name)
    value = float(value)
    if not math.isfinite(value) or value < 0 or (maximum is not None and value > maximum):
        raise ValueError(name)
    return value


def clean_product(body):
    if not isinstance(body, dict):
        raise ValueError('product')
    out = {k: str(body.get(k) or '').strip()[:limit] for k, limit in
           [('name',160),('offer',3000),('url',2000),('account_id',32),('tracking_key',64)]}
    if not out['name']:
        raise ValueError('Informe o nome do produto.')
    if out['url'] and not out['url'].startswith(('https://','http://')):
        raise ValueError('Informe o endereço completo da página do produto.')
    if out['account_id'] and not re.fullmatch(r'\d{1,32}',out['account_id']):
        raise ValueError('Conta de anúncios inválida.')
    if out['tracking_key'] and not re.fullmatch(r'[a-f0-9]{32,64}',out['tracking_key']):
        raise ValueError('Identificador de rastreamento inválido.')
    currency=str(body.get('currency') or 'BRL').upper()
    if not re.fullmatch('[A-Z]{3}',currency):
        raise ValueError('Moeda inválida.')
    out['currency']=currency
    out['price']=number(body.get('price'),'Preço')
    if out['price'] is not None and out['price']<=0:
        raise ValueError('O preço deve ser maior que zero.')
    for key in COSTS:
        out[key]=number(body.get(key),key,100 if key.endswith('_pct') else None)
    ids=body.get('campaign_ids') or []
    if not isinstance(ids,list) or len(ids)>100 or any(not re.fullmatch(r'\d{1,32}',str(x)) for x in ids):
        raise ValueError('Seleção de campanhas inválida.')
    out['campaign_ids']=list(dict.fromkeys(map(str,ids)))
    draft=body.get('draft') or {}
    if not isinstance(draft,dict):raise ValueError('Rascunho inválido.')
    out['draft']={k:str(draft.get(k) or '')[:3000] for k in (
        'name','objective','country','age_min','age_max','message','headline','image_url','page_id',
        'campaign_id','adset_id','ad_id','stage','created_hash','pixel_id','pending_action')}
    out['draft']['budget']=number(draft.get('budget'),'Orçamento diário')
    return out


def financial(product, metrics):
    missing=[k for k in ('price',*COSTS) if product.get(k) is None]
    if missing:return {'status':'costs_required','missing':missing}
    p=product
    threshold=finance.calc_breakeven(p['price'],p['fee_pct'],p['fee_fixed'],
        p['unit_cost']+p['other_costs']+p['price']*p['tax_pct']/100,p['margin_pct'])
    out={'status':'thresholds_only',**threshold,'received_revenue':None,
         'revenue_basis':'Meta attribution, not confirmed cash receipts',
         'net_profit_attributed':None,'roi':None}
    if metrics is None:return out
    spend,revenue,purchases=[metrics.get(k) for k in ('spend','revenue','purchases')]
    if any(x is None for x in (spend,revenue,purchases)):return out
    costs=purchases*(p['unit_cost']+p['fee_fixed']+p['other_costs'])+revenue*(p['fee_pct']+p['tax_pct'])/100
    profit=revenue-costs-spend
    out.update(status='estimated_from_attribution',net_profit_attributed=round(profit,2),
        modeled_costs=round(costs,2),roi=round(profit/(spend+costs)*100,2) if spend+costs>0 else None,
        roi_formula='estimated net profit / (ad spend + modeled costs)',
        cpa=round(spend/purchases,2) if purchases>0 else None,
        roas=round(revenue/spend,4) if spend>0 else None)
    return out


def _purchase(values):
    # Meta can return overlapping purchase aliases. Never sum those aliases.
    for kind in ('omni_purchase','purchase','offsite_conversion.fb_pixel_purchase'):
        found=[x for x in (values or []) if x.get('action_type')==kind]
        if found:return sum(float(x.get('value') or 0) for x in found)
    return 0.0


def register(app, deps):
    sb, target, directory, mcp = [deps[k] for k in ('sb','target','directory','mcp')]

    def rows(email):
        if target()[0]:
            return sb('GET','ad_drafts',params={'owner_email':'eq.'+email,'structure_slug':'eq.'+SLUG,
                      'select':'id,briefing,updated_at','order':'updated_at.desc','limit':'200'}) or []
        with LOCK:
            path=directory()/'business_workspace.json'
            return json.loads(path.read_text(encoding='utf-8')).get(email,[]) if path.exists() else []

    def get_product(email,pid):
        row=next((r for r in rows(email) if r['id']==pid),None)
        if not row:raise HTTPException(404,'Produto não encontrado nesta conta.')
        return {'id':row['id'],**row['briefing']}

    def save(email,body):
        if not isinstance(body,dict):raise HTTPException(400,'Produto inválido.')
        pid=body.get('id')
        if pid:get_product(email,pid)  # Never upsert someone else's ID.
        else:pid='biz_'+hashlib.sha256((email+secrets.token_hex(24)).encode()).hexdigest()[:48]
        try:p=clean_product(body)
        except (ValueError,TypeError) as exc:raise HTTPException(400,str(exc))
        row={'id':pid,'owner_email':email,'structure_slug':SLUG,'structure_name':p['name'],
             'briefing':p,'updated_at':datetime.now(timezone.utc).isoformat()}
        if target()[0]:sb('POST','ad_drafts',payload=row)
        else:
            with LOCK:
                path=directory()/'business_workspace.json'
                data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
                data[email]=[r for r in data.get(email,[]) if r['id']!=pid]+[row]
                tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');tmp.replace(path)
        return {'id':pid,**p}

    def read_tool(email,name,args):
        result=mcp(name,args,email)
        if not result or result.get('isError'):raise HTTPException(502,'Não foi possível consultar os dados autorizados do Meta Ads.')
        try:return json.loads(next(c['text'] for c in result.get('content',[]) if c.get('type')=='text'))
        except (StopIteration,ValueError,KeyError):raise HTTPException(502,'Resposta Meta inválida.')

    def context(email,body):
        product=get_product(email,str(body.get('product_id') or ''))
        preset=str(body.get('preset') or 'today')
        if preset not in PRESETS:raise HTTPException(400,'Período inválido.')
        aid=str(body.get('account_id') or product.get('account_id') or '')
        out={'read_only':True,'product':product,'preset':preset,'account':None,'campaigns':[],
             'metrics':None,'financial':financial(product,None),'errors':[],
             'sources':{'product_costs':'user supplied','metrics':'Meta Ads authorized API','received_revenue':'unavailable'}}
        if not aid:
            out['errors'].append('Conecte e selecione a conta Meta no cadastro do produto. O contexto da oferta e dos custos continua disponível.')
            return out
        try:
            accounts=read_tool(email,'list_ad_accounts',{}).get('ad_accounts',[])
            account=next((a for a in accounts if str(a.get('account_id'))==aid),None)
            if not account:raise HTTPException(403,'Selecione uma conta Meta pertencente a este utilizador.')
            out['account']=account
            campaigns=read_tool(email,'list_objects',{'ad_account_id':aid,'level':'campaigns','limit':100}).get('items',[])
            out['campaigns']=campaigns
            ids=product['campaign_ids']
            if any(i not in {str(c.get('id')) for c in campaigns} for i in ids):
                raise HTTPException(403,'Uma campanha selecionada não pertence à conta ou não pôde ser confirmada.')
            if not ids:
                out['errors'].append('Vincule as campanhas do produto para calcular lucro sem misturar produtos da conta.')
                return out
            if account.get('currency')!=product['currency']:
                out['errors'].append('A moeda do produto difere da moeda da conta; não foi feita conversão nem soma.')
                return out
            data=read_tool(email,'get_insights',{'ad_account_id':aid,'date_preset':preset,'level':'campaign'})
            if data.get('incomplete'):
                out['errors'].append('A consulta Meta retornou dados paginados incompletos. O cálculo foi suspenso para não subestimar resultados.')
                return out
            selected=[r for r in data.get('rows',[]) if str(r.get('campaign_id')) in ids]
            metrics={k:sum(float(r.get(k) or 0) for r in selected) for k in ('spend','impressions','clicks')}
            metrics.update(purchases=sum(_purchase(r.get('actions')) for r in selected),
                revenue=sum(_purchase(r.get('action_values')) for r in selected),currency=product['currency'],
                campaign_ids=ids,scope='selected product campaigns')
            # No returned rows means no delivery for confirmed campaigns. Missing fields
            # in returned rows remain unknown instead of becoming invented zeros.
            for field,key in [('actions','purchases'),('action_values','revenue')]:
                if any(field not in r for r in selected):metrics[key]=None
            for key in ('spend','impressions','clicks'):
                if any(key not in r for r in selected):metrics[key]=None
            spend,clicks,impressions=[metrics[k] for k in ('spend','clicks','impressions')]
            metrics.update(cpc=spend/clicks if spend is not None and clicks else None,
                cpm=spend/impressions*1000 if spend is not None and impressions else None,
                ctr=clicks/impressions*100 if clicks is not None and impressions else None)
            out['metrics']=metrics;out['financial']=financial(product,metrics)
        except HTTPException as exc:
            if exc.status_code==403:raise
            out['errors'].append(exc.detail)
        return out

    @app.get('/api/workspace/products')
    def list_products(request:Request):
        return {'products':[{'id':r['id'],**r['briefing']} for r in rows(request.state.user_email)]}

    @app.post('/api/workspace/products')
    async def save_product(request:Request):
        body=await request.json()
        return {'product':await run_in_threadpool(save,request.state.user_email,body)}

    @app.post('/api/workspace/context')
    def get_context(request:Request,body:dict):
        return context(request.state.user_email,body)

    deps['context']=context


