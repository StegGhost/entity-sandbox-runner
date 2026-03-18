
import os, json, random
from install.preflight_strict import run_preflight

STATE="logs/state.json"

def load():
    if not os.path.exists(STATE):
        return {"cycles":0,"u":[]}
    try:
        return json.load(open(STATE))
    except:
        return {"cycles":0,"u":[]}

def save(s):
    os.makedirs("logs",exist_ok=True)
    json.dump(s,open(STATE,"w"),indent=2)

def main():
    p = run_preflight()
    print("PREFLIGHT:",p)

    if p["status"] != "pass":
        raise Exception("STRICT PREFLIGHT FAILED")

    s=load()
    s["cycles"]+=1

    u=random.uniform(0.5,0.9)
    s["u"].append(u)
    s["u"]=s["u"][-20:]

    receipt={
        "cycle":s["cycles"],
        "u":u,
        "status":"ok"
    }

    os.makedirs("payload/receipts",exist_ok=True)
    json.dump(receipt,open(f"payload/receipts/r_{s['cycles']:04d}.json","w"),indent=2)

    save(s)
    print("SUMMARY:",receipt)

if __name__=="__main__":
    main()
