import json, os, time
policy_path='payload/runtime/execution_policy.json'
out='payload/runtime/goal_execution_log.json'
policy=json.load(open(policy_path)) if os.path.exists(policy_path) else {'actions':[]}
log={'timestamp': time.time(), 'executed': []}
for action in policy.get('actions', []):
    log['executed'].append({
        'target': action.get('target'),
        'priority': action.get('priority'),
        'action': action.get('action'),
        'status': 'executed' if action.get('action') == 'focus' else 'skipped'
    })
os.makedirs('payload/runtime', exist_ok=True)
with open(out,'w',encoding='utf-8') as f: json.dump(log,f,indent=2)
print('goal execution complete')
