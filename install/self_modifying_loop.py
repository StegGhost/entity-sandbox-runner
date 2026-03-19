import json, os, time
cfg_path='config/autonomous_loop_config.json'
cfg=json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
cfg['last_updated']=time.time(); cfg['auto_tuned']=True
os.makedirs('config', exist_ok=True)
with open(cfg_path,'w',encoding='utf-8') as f: json.dump(cfg,f,indent=2)
print('loop config updated')
