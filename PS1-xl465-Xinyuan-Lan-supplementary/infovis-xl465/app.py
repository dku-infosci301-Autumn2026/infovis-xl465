from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import json,os,time
from engine import Engine
ROOT=Path(__file__).resolve().parent
engine=Engine(model=os.getenv('DISABLE_MODEL')!='1')
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def send_json(self,obj,status=200):
  data=json.dumps(obj).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_GET(self):
  if self.path=='/api/status':return self.send_json({'semantic_ready':engine.session is not None,'model':engine.catalog['manifest']['model'],'scope':engine.catalog['manifest']['counts']})
  return super().do_GET()
 def do_POST(self):
  if self.path!='/api/search':return self.send_json({'error':'Not found'},404)
  try:
   size=int(self.headers.get('Content-Length','0'))
   if size>4096:return self.send_json({'error':'Request too large'},413)
   p=json.loads(self.rfile.read(size));t=time.perf_counter();r=engine.search(str(p.get('query','')),p.get('method','semantic'),bool(p.get('additional',True)),p.get('system','all'));r['elapsed_ms']=round((time.perf_counter()-t)*1000,2);return self.send_json(r)
  except (ValueError,TypeError,json.JSONDecodeError) as e:return self.send_json({'error':str(e)},400)
  except Exception:return self.send_json({'error':'Search failed. Retry or use keyword search.'},500)
if __name__=='__main__':
 port=int(os.getenv('PORT','7860'));print(f'VA-Blueprint Task Explorer on port {port}; semantic={engine.session is not None}',flush=True);ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
