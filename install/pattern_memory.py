import json, os, time
inp='payload/runtime/priority_weights.json'
out='payload/runtime/pattern_memory.json'
data=json.load(open(inp)) if os.path.exists(inp) else {'items':[]}
mem={'timestamp': time.time(), 'patterns': []}
for item in data.get('items', []):
    mem['patterns'].append({'text': item.get('text'), 'score': item.get('score')})
os.makedirs('payload/runtime', exist_ok=True)
with open(out,'w',encoding='utf-8') as f: json.dump(mem,f,indent=2)
print('memory updated')
