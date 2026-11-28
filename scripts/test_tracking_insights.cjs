const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const T=require('../static/tracking-insights.js');
const rows=[
  {id:'paid-1',ts:100,status:'paid',amount:97,currency:'BRL',utm_source:'facebook',utm_campaign:'Campanha A',capi_event:'Purchase',capi_status:'sent',capi_event_id:'paid-1'},
  {id:'paid-2',ts:101,status:'paid',amount:20,currency:'USD',utm_source:'google',utm_campaign:'Campanha B',capi_status:'error:fixture'},
  {id:'paid-3',ts:102,status:'paid',amount:50,currency:'BRL',utm_source:'facebook',capi_status:'no_credentials'},
  {id:'pending-1',ts:103,status:'pending',amount:1000,currency:'BRL'},
  {id:'refund-1',ts:104,status:'refunded',amount:30,currency:'BRL'},
];
test('paid revenue excludes pending and refunds; currencies remain separate',()=>{
  const s=T.summarize(rows);assert.equal(s.totals.BRL.revenue,147);assert.equal(s.totals.USD.revenue,20);
  assert.equal(s.paid,3);assert.equal(s.totals.BRL.refunded,1);
});
test('exact retries collapse; unrelated sales with same amount remain distinct',()=>{
  assert.equal(T.unique([...rows,rows[0],{...rows[0],id:'different'}]).length,6);
});
test('missing values and unknown currencies do not become invented revenue',()=>{
  const s=T.summarize([{status:'paid',amount:null,currency:'BRL'},{status:'paid',amount:10},{status:'paid',amount:20}]);
  assert.equal(s.totals.BRL.unknownAmount,1);assert.equal(s.totals.UNKNOWN.revenue,null);
  for(const amount of [null,undefined,true,false,[],{},' ',NaN,Infinity,-1])assert.equal(T.amount({amount}),null);
});
test('UTM diagnosis distinguishes complete, partial, absent without inferring organic traffic',()=>{
  assert.equal(T.coverage(rows[0]),'complete');assert.equal(T.coverage(rows[2]),'partial');assert.equal(T.coverage(rows[3]),'missing');
  assert.ok(Math.abs(T.summarize(rows).coverage-200/3)<1e-9);
});
test('filters combine time boundaries, currency, state and text',()=>{
  assert.deepEqual(T.filter(rows,{since:100,until:102,currency:'BRL',status:'paid',query:'campanha a'}).map(x=>x.id),['paid-1']);
  assert.deepEqual(T.filter(rows,{coverage:'partial'}).map(x=>x.id),['paid-3']);
});
test('API acceptance is not counted as attribution or deduplication proof',()=>{
  const s=T.summarize(rows);assert.equal(s.capiAccepted,1);assert.equal(s.capiErrors,1);assert.equal(s.capiMissingCredentials,1);
  assert.equal(s.deduplicated,undefined);assert.equal(s.roas,undefined);
});
test('empty data has no fictitious coverage percentage',()=>{assert.equal(T.summarize([]).coverage,null)});
test('safe URL generation preserves unrelated query parameters and fragment',()=>{
  const url=new URL(T.trackedUrl('https://example.com/oferta?coupon=REAL#checkout',{utm_source:'facebook',utm_medium:'paid_social',utm_campaign:'Campanha São Paulo'}));
  assert.equal(url.searchParams.get('coupon'),'REAL');assert.equal(url.hash,'#checkout');assert.equal(url.searchParams.get('utm_campaign'),'Campanha São Paulo');
});
test('unsafe links, credentials and missing identification are rejected',()=>{
  for(const base of ['javascript:alert(1)','https://user:password@example.com'])assert.throws(()=>T.trackedUrl(base,{utm_source:'x',utm_campaign:'y'}));
  assert.throws(()=>T.trackedUrl('https://example.com',{utm_source:'x'}));
});
test('CSV quotes cells and neutralizes spreadsheet formula injection',()=>{
  const csv=T.csv([{id:'=HYPERLINK("bad")',utm_source:' \t+SUM(1;1)',utm_campaign:'a;"b"\nc'}]);
  assert.ok(csv.startsWith('\uFEFF'));assert.ok(csv.includes("\"'=HYPERLINK"));assert.ok(csv.includes("' \t+SUM"));assert.ok(csv.includes('a;""b""\nc'));
  assert.ok(!T.csv([{capi_status:'error:private diagnostic'}]).includes('private diagnostic'));
});
test('invalid rows are ignored and known numeric zero remains valid',()=>{
  assert.equal(T.unique([null,undefined,[],rows[0]]).length,1);assert.equal(T.amount({amount:0}),0);
});
test('embedded source is exactly the module tested here',()=>{
  const page=fs.readFileSync(path.join(__dirname,'../static/index.html'),'utf8').replace(/\r\n/g,'\n');
  const code=page.split('// TRACKING INSIGHTS START\n')[1].split('\n// TRACKING INSIGHTS END')[0];
  assert.equal(code,fs.readFileSync(path.join(__dirname,'../static/tracking-insights.js'),'utf8').replace(/\r\n/g,'\n'));
});
