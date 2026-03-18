import json, os
def record_cycle(state,results,action,u):
    os.makedirs("payload/replay",exist_ok=True)
    json.dump({"state":state,"results":results,"action":action,"u":u},
              open(f"payload/replay/c_{state['cycles']:04d}.json","w"), indent=2)
