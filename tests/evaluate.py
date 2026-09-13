import sys,json,time,hashlib,platform
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import Engine,ROOT
start=time.perf_counter();e=Engine();load=time.perf_counter()-start
assert e.session is not None,e.error
q=json.loads((ROOT/'tests/queries.json').read_text());rows=[]
for method in ['keyword','semantic']:
 for additional in [False,True]:
  for case in q:
   t=time.perf_counter();r=e.search(case['query'],method,additional);ms=(time.perf_counter()-t)*1000;ids=[x['id'] for x in r['results']];ranks=[ids.index(x)+1 for x in case['acceptable'] if x in ids];rank=min(ranks) if ranks else None
   rows.append({'query_id':case['id'],'condition':('K' if method=='keyword' else 'S')+str(int(additional)),'top3_hit':rank is not None and rank<=3,'rank':rank,'reciprocal_rank':1/rank if rank else 0,'elapsed_ms':round(ms,2),'results':r['results']})
summary={}
for c in ['K0','K1','S0','S1']:
 rr=[r for r in rows if r['condition']==c];summary[c]={'top3_hits':sum(r['top3_hit'] for r in rr),'n':len(rr),'mrr_at6':round(sum(r['reciprocal_rank'] for r in rr)/len(rr),3),'median_ms':round(sorted(r['elapsed_ms'] for r in rr)[len(rr)//2],2)}
ids={n['id'] for n in e.nodes};assert len(ids)==len(e.nodes)
assert all(x['source'] in ids and x['target'] in ids for x in e.catalog['edges'])
assert all(n in ids for ex in e.catalog['examples'] for n in ex['component_ids'])
assert e.search('')['results']==[]
try:e.search('x'*501);raise AssertionError('length limit absent')
except ValueError:pass
fallback=Engine(model=False).search('line chart');assert fallback['method']=='keyword' and 'fallback' in fallback['notice']
neg=e.search('How can I bake sourdough bread at home?')
import onnxruntime,tokenizers,numpy
out={'date_utc':'2026-09-13','protocol_sha256':hashlib.sha256((ROOT/'tests/PROTOCOL.md').read_bytes()).hexdigest(),'queries_sha256':hashlib.sha256((ROOT/'tests/queries.json').read_bytes()).hexdigest(),'environment':{'python':platform.python_version(),'platform':platform.platform(),'onnxruntime':onnxruntime.__version__,'tokenizers':tokenizers.__version__,'numpy':numpy.__version__,'provider':'CPUExecutionProvider','threads':2,'initialization_seconds':round(load,3)},'summary':summary,'rows':rows,'checks':{'unique_component_ids':True,'edge_endpoints':True,'mapping_endpoints':True,'empty_query':True,'length_limit':True,'model_failure_fallback':True},'unrelated_query':neg,'success_criterion_met':summary['S1']['top3_hits']>=8 and summary['S1']['top3_hits']>summary['K0']['top3_hits'],'limitations':['AI-authored fixtures and relevance labels; not independent judgments.','No student or community participants.','Small purposively selected subset, not generalization to 101 systems.','Latency is one local environment and one pass; not human task time.','Source mappings and source-paper truth require student verification.']}
(ROOT/'evidence/retrieval-results.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['summary','checks','unrelated_query','success_criterion_met']},indent=2))
