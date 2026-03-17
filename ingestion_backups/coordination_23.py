import random
AVAILABLE_WORKERS=['w1','w2','w3']
def initialize_workers(s):
 w=s.setdefault('workers',{})
 [w.setdefault(x,{'score':0.5,'count':0,'failures':0}) for x in AVAILABLE_WORKERS]
def select_worker(s): initialize_workers(s);return random.choice(list(s['workers'].keys()))
def reassign_if_failed(s,r): return r['worker'] if r['decision']!='fail' else 'w2'
