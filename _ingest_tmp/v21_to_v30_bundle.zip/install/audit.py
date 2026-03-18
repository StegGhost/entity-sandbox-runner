
import json, os
LOG="logs/audit.json"
def record(event):
    os.makedirs("logs",exist_ok=True)
    data=[]
    if os.path.exists(LOG):
        try: data=json.load(open(LOG))
        except: data=[]
    data.append(event)
    json.dump(data,open(LOG,"w"),indent=2)
