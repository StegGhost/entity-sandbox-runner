import json, os, time, hashlib
cfg_path='config/actuator_bridge_config.json'
try:
    cfg=json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
except Exception:
    cfg={}
goal_log=cfg.get('goal_execution_log','payload/runtime/goal_execution_log.json')
act_root=cfg.get('actuator_root','payload/actuation')
receipts_root=cfg.get('receipts_root','payload/receipts/actuator_bridge')
max_actions=int(cfg.get('max_actions',25))
log=json.load(open(goal_log)) if os.path.exists(goal_log) else {'executed':[]}
os.makedirs(act_root, exist_ok=True); os.makedirs(receipts_root, exist_ok=True)
outputs=[]
for idx,action in enumerate(log.get('executed',[])[:max_actions],1):
    target=action.get('target',f'action_{idx}')
    slug=''.join(ch.lower() if ch.isalnum() else '_' for ch in target)[:80].strip('_') or 'unnamed_action'
    path=os.path.join(act_root,f'{idx:04d}_{slug}.json')
    artifact={'timestamp':time.time(),'target':target,'priority':action.get('priority'),'action':action.get('action'),'status':action.get('status'),'actuation_type':'repo_artifact','effect':'materialized_action_record'}
    with open(path,'w',encoding='utf-8') as f: json.dump(artifact,f,indent=2)
    outputs.append(path)
summary=os.path.join(act_root,'actuation_summary.md')
with open(summary,'w',encoding='utf-8') as f:
    f.write('# Actuation Summary\n\n- generated_artifacts: %d\n\n' % len(outputs) + '\n'.join('- '+p for p in outputs))
receipt={'type':'actuator_bridge','timestamp':time.time(),'goal_execution_log':goal_log,'generated_artifacts':outputs,'summary_md':summary}
receipt['hash']=hashlib.sha256(json.dumps(receipt,sort_keys=True).encode('utf-8')).hexdigest()
existing=sorted(f for f in os.listdir(receipts_root) if f.startswith('actuator_bridge_') and f.endswith('.json'))
rp=os.path.join(receipts_root,f'actuator_bridge_{len(existing)+1:04d}.json')
with open(rp,'w',encoding='utf-8') as f: json.dump(receipt,f,indent=2)
print(json.dumps({'status':'ok','generated_artifacts':len(outputs),'summary_md':summary,'receipt_path':rp},indent=2))
