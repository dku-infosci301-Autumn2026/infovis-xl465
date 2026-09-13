import json, urllib.request, hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
root=Path(__file__).resolve().parent; rev='831e308cf9feba791db0c279dea5f7983ca98445'; mrev='1110a243fdf4706b3f48f1d95db1a4f5529b4d41'
specs=['line','point_2d','histogram','interactive_brush','interactive_overview_detail','interactive_query_widgets']
jobs=[(f'https://raw.githubusercontent.com/vega/vega-lite/{rev}/examples/specs/{n}.vl.json',root/'data/examples'/f'{n}.vl.json') for n in specs]
jobs += [(f'https://raw.githubusercontent.com/vega/vega-lite/{rev}/LICENSE',root/'data/examples/LICENSE'),(f'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/{mrev}/tokenizer.json',root/'models/tokenizer.json'),(f'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/{mrev}/README.md',root/'models/README.md'),(f'https://raw.githubusercontent.com/urban-toolkit/va-blueprint/b4b9bd7f7b46c49a44eb7306eafb72e7a0dad1b7/README.md',root/'data/blueprints/UPSTREAM_README.md')]
def get(job):
 url,p=job
 if not p.exists():
  with urllib.request.urlopen(url,timeout=40) as r:p.write_bytes(r.read())
 return str(p)
with ThreadPoolExecutor(max_workers=6) as ex:
 for p in ex.map(get,jobs):print(p)
mapping={
'line':['urbanpulse:12','taxivis:9'],
'point_2d':['urbanpulse:11','taxivis:11'],
'histogram':['taxivis:10'],
'interactive_brush':['urbanpulse:13'],
'interactive_overview_detail':['taxivis:13'],
'interactive_query_widgets':['taxivis:14']}
examples=[]
for n in specs:
 spec=json.loads((root/'data/examples'/f'{n}.vl.json').read_text())
 examples.append({'id':n,'description':spec.get('description',''),'filename':f'{n}.vl.json','url':f'https://vega.github.io/vega-lite/examples/{n}.html','source_url':f'https://github.com/vega/vega-lite/blob/{rev}/examples/specs/{n}.vl.json','component_ids':mapping[n],'mapping_status':'AI-assisted proposed analogy; not source-system implementation; student review pending','spec':spec})
(root/'data/examples.json').write_text(json.dumps(examples,indent=2))
nodes=[]; edges=[]; systems=[]
for p in sorted((root/'data/blueprints').glob('*.json')):
 d=json.loads(p.read_text()); system=p.stem; systems.append({'id':system,'title':d['PaperTitle'],'year':d['Year']})
 for h in d['HighBlocks']:
  for inter in h['IntermediateBlocks']:
   for n in inter['GranularBlocks']:
    node={'id':f"{system}:{n['ID']}",'system':system,'number':n['ID'],'name':n['GranularBlockName'],'stage':h['HighBlockName'],'group':inter['IntermediateBlockName'],'description':n['PaperDescription'],'inputs':n.get('Inputs',[]),'outputs':n.get('Outputs',[]),'citation':n.get('ReferenceCitation',''),'examples':[e['id'] for e in examples if f"{system}:{n['ID']}" in e['component_ids']]}
    nodes.append(node)
    for target in n.get('FeedsInto',[]):edges.append({'source':node['id'],'target':f'{system}:{target}','kind':'interaction' if h['HighBlockName']=='Interaction' else 'data','kind_rule':'derived from source stage; not explicit edge typing'})
manifest={'prepared_utc':'2026-09-13','blueprint_revision':'b4b9bd7f7b46c49a44eb7306eafb72e7a0dad1b7','vega_revision':rev,'model':'sentence-transformers/all-MiniLM-L6-v2','model_revision':mrev,'onnx_file':'onnx/model_quint8_avx2.onnx','scope':'Two illustrative systems only; no claim about all 101 systems','blueprint_license':'MIT stated in upstream README; no standalone LICENSE in inspected commit','vega_license':'BSD-3-Clause','model_license':'Apache-2.0 per model card','counts':{'systems':len(systems),'nodes':len(nodes),'edges':len(edges),'examples':len(examples),'mapped_nodes':sum(bool(n['examples']) for n in nodes)},'sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}}
(root/'data/catalog.json').write_text(json.dumps({'systems':systems,'nodes':nodes,'edges':edges,'examples':examples,'manifest':manifest},indent=2))
(root/'data/manifest.json').write_text(json.dumps(manifest,indent=2));print(manifest['counts'])
