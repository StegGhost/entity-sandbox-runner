import json, os, time

inp='payload/runtime/priority_weights.json'
out='payload/runtime/execution_policy.json'

data=json.load(open(inp)) if os.path.exists(inp) else {'items':[]}
policy={'timestamp': time.time(), 'actions': []}
for item in data.get('items', [])[:10]:
    policy['actions'].append({
        'target': item.get('text'),
        'priority': item.get('score'),
        'action': 'focus' if item.get('score', 0) >= 2 else 'monitor'
    })
os.makedirs('payload/runtime', exist_ok=True)
with open(out,'w',encoding='utf-8') as f: json.dump(policy,f,indent=2)
print('policy generated')
