import json,os,time,hashlib

def write_receipt(d,s,r,summary):
 os.makedirs(d,exist_ok=True)
 payload={'ts':time.time(),'cycle':s.get('cycles'),'u_signal':summary.get('u_signal'),'action':summary.get('action'),'results_hash':hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()}
 payload['receipt_hash']=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
 path=os.path.join(d,f"receipt_{s.get('cycles',0):04d}.json")
 open(path,'w').write(json.dumps(payload,indent=2));return path
