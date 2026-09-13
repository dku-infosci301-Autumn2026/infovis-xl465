"""Local retrieval. No model training, API key, or generated answers."""
import json, math, re, threading
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
STOP=set('a an the i we you my to of for and or in on with how can do does is are that this it by from as want would like'.split())
def tokens(text):return [x for x in re.findall(r'[a-z0-9]+',text.lower()) if x not in STOP]
class Engine:
 def __init__(self,model=True):
  self.catalog=json.loads((ROOT/'data/catalog.json').read_text()); self.nodes=self.catalog['nodes'];self.examples={x['id']:x for x in self.catalog['examples']};self.lock=threading.Lock();self.session=None;self.error=None
  self.docs={False:[self.document(n,False) for n in self.nodes],True:[self.document(n,True) for n in self.nodes]}
  if model:
   try:
    import onnxruntime as ort
    from tokenizers import Tokenizer
    opt=ort.SessionOptions();opt.intra_op_num_threads=2;opt.inter_op_num_threads=1
    self.session=ort.InferenceSession(str(ROOT/'models/model.onnx'),sess_options=opt,providers=['CPUExecutionProvider'])
    self.tokenizer=Tokenizer.from_file(str(ROOT/'models/tokenizer.json'));self.tokenizer.enable_truncation(max_length=256);self.tokenizer.enable_padding()
    self.emb={a:self.encode(d) for a,d in self.docs.items()}
   except Exception as e:self.error=f'{type(e).__name__}: {e}';self.session=None
 def document(self,n,additional):
  s=' '.join([n['name'],n['stage'],n['group'],n['description'],' '.join(n['inputs']),' '.join(n['outputs'])])
  if additional:
   for ex in n['examples']:
    e=self.examples[ex];s+=' Example: '+ex.replace('_',' ')+' '+e['description']
  return s
 def encode(self,texts):
  vectors=[]
  with self.lock:
   for off in range(0,len(texts),8):
    enc=self.tokenizer.encode_batch(texts[off:off+8]);ids=np.array([e.ids for e in enc],dtype=np.int64);mask=np.array([e.attention_mask for e in enc],dtype=np.int64)
    all_inputs={'input_ids':ids,'attention_mask':mask,'token_type_ids':np.zeros_like(ids)}
    out=self.session.run(None,{n.name:all_inputs[n.name] for n in self.session.get_inputs()})[0]
    pooled=(out*mask[:,:,None]).sum(1)/np.maximum(mask.sum(1)[:,None],1) if out.ndim==3 else out
    pooled=pooled/np.maximum(np.linalg.norm(pooled,axis=1,keepdims=True),1e-9);vectors.extend(pooled)
  return np.array(vectors)
 def bm25(self,q,additional):
  docs=[tokens(s) for s in self.docs[additional]];qt=set(tokens(q));avg=sum(map(len,docs))/len(docs);scores=[]
  for d in docs:
   score=0
   for t in qt:
    f=d.count(t);df=sum(t in x for x in docs);idf=math.log(1+(len(docs)-df+.5)/(df+.5));score+=idf*(f*2.5)/(f+1.5*(.25+.75*len(d)/avg)) if f else 0
   scores.append(score)
  return scores
 def search(self,q,method='semantic',additional=True,system='all'):
  q=q.strip()
  if len(q)>500:raise ValueError('Please use 500 characters or fewer.')
  if method not in ['semantic','keyword']:raise ValueError('Unknown search method.')
  if system not in ['all','taxivis','urbanpulse']:raise ValueError('Unknown system.')
  if not q:return {'results':[],'method':method,'additional':additional,'notice':'Enter a task to search.'}
  fallback=method=='semantic' and self.session is None;actual='keyword' if fallback else method
  scores=self.bm25(q,additional) if actual=='keyword' else self.emb[additional]@self.encode([q])[0]
  threshold=0 if actual=='keyword' else .30
  ranked=sorted([(float(scores[i]),n) for i,n in enumerate(self.nodes) if system=='all' or n['system']==system],key=lambda x:(-x[0],x[1]['id']))
  matches=[{'id':n['id'],'score':round(s,6),'name':n['name'],'system':n['system'],'examples':n['examples'] if additional else []} for s,n in ranked if s>threshold][:6]
  return {'results':matches,'method':actual,'requested_method':method,'additional':additional,'notice':('Semantic model unavailable; keyword fallback is active.' if fallback else 'Similarity suggests candidates; it does not verify correctness.' if actual=='semantic' else 'Keyword matching across the same component descriptions.'),'threshold':threshold}
