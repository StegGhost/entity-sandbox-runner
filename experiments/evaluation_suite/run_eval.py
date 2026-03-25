
import json, os, random, hashlib, time

STATE_FILE = "logs/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except:
            return {"cycles":0,"last_receipt":None,"history":[]}
    return {"cycles":0,"last_receipt":None,"history":[]}

def save_state(s):
    os.makedirs("logs", exist_ok=True)
    json.dump(s, open(STATE_FILE, "w"), indent=2)

def hash_payload(p):
    raw = json.dumps(p, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()

def sign_payload(p):
    raw = json.dumps(p, sort_keys=True)
    return hashlib.sha256((raw + "dev-key").encode()).hexdigest()

def run_cycle():
    results=[]
    for s in ["s1","s2","s3"]:
        c=random.uniform(0.5,0.9)
        d="ok" if c>0.6 else "fail"
        results.append({"shard":s,"confidence":c,"decision":d})
    return results

def compute_u(results):
    return sum(r["confidence"] for r in results)/len(results)

def load_policy():
    p="config/policy.json"
    if os.path.exists(p):
        return json.load(open(p))
    return {"hard_stop_u":0.3,"restrict_u":0.6,"allow_u":0.85}

def enforce(policy,u):
    if u < policy.get("hard_stop_u",0.3):
        return "halt","hard_stop"
    if u < policy.get("restrict_u",0.6):
        return "restrict","mid"
    if u < policy.get("allow_u",0.85):
        return "allow","ok"
    return "allow","strong"

def main():
    s=load_state()
    s["cycles"]+=1

    results=run_cycle()
    u=compute_u(results)

    policy=load_policy()
    action,reason=enforce(policy,u)

    receipt={
        "cycle":s["cycles"],
        "u":u,
        "action":action,
        "reason":reason,
        "prev_hash":s.get("last_receipt")
    }

    receipt["hash"]=hash_payload(receipt)
    receipt["signature"]=sign_payload(receipt)

    os.makedirs("payload/receipts",exist_ok=True)
    path=f"payload/receipts/r_{s['cycles']:04d}.json"
    json.dump(receipt, open(path,"w"), indent=2)

    s["last_receipt"]=receipt["hash"]
    s["history"].append(receipt)
    save_state(s)

    print("SUMMARY:", receipt)

if __name__=="__main__":
    main()
