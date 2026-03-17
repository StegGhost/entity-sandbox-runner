
import json, os, time, hashlib, random
from install.policy_engine import load_policy, enforce_policy
from install.crypto import sign_payload, hash_payload
from install.replay import record_cycle

STATE_FILE = "logs/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {"cycles":0,"last_receipt":None,"history":[]}

def save_state(state):
    json.dump(state, open(STATE_FILE,"w"), indent=2)

def run_cycle():
    results=[]
    for s in ["s1","s2","s3"]:
        c=random.uniform(0.5,0.9)
        d="ok" if c>0.6 else "fail"
        results.append({"shard":s,"confidence":c,"decision":d})
    return results

def compute_u(results):
    return sum(r["confidence"] for r in results)/len(results)

def main():
    state=load_state()
    state["cycles"]+=1

    results=run_cycle()
    u=compute_u(results)

    policy=load_policy()
    action,reason=enforce_policy(policy,state,u)

    receipt={
        "cycle":state["cycles"],
        "u":u,
        "action":action,
        "prev_hash":state.get("last_receipt")
    }

    receipt["hash"]=hash_payload(receipt)
    receipt["signature"]=sign_payload(receipt)

    os.makedirs("payload/receipts",exist_ok=True)
    path=f"payload/receipts/r_{state['cycles']:04d}.json"
    json.dump(receipt, open(path,"w"), indent=2)

    state["last_receipt"]=receipt["hash"]
    state["history"].append(receipt)
    save_state(state)

    record_cycle(state,results,action,u)

    print("SUMMARY:", receipt)

if __name__=="__main__":
    main()
