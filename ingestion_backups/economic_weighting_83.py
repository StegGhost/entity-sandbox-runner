def weighted_score(state):
 h=state.get('history',[])[-20:]
 return 0.5 if not h else sum(x['confidence'] for x in h)/len(h)
def weighted_mode(state,u,a):
 return 'conservative' if a=='restrict' or u<0.6 else 'aggressive' if u>0.84 else 'normal'
