import json, os, random

from install.receipt_guard import validate_and_repair
from install.node_identity import get_node_id
from install.policy_engine import load_policy
from install.bcat_engine import enforce_bcat
from install.crypto_keys import sign_with_keypair
from install.network_registry import get_peer_receipts
from install.peer_verification import verify_peer_receipt
from install.reputation_decay import decay
from install.anomaly import detect_anomaly
from install.policy_voting import vote
from install.audit import record
from install.drift import drift
from install.quorum import quorum
from install.arbitration import arbitrate

STATE="logs/state.json"

def load():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"cycles":0,"u":[],"trust":{}}

def save(s):
    os.makedirs("logs",exist_ok=True)
    json.dump(s,open(STATE,"w"),indent=2)

def main():
    s=load()
    s["cycles"]+=1

    u=random.uniform(0.5,0.9)
    s["u"].append(u)
    s["u"]=s["u"][-20:]

    policy=load_policy()
    local,reason=enforce_bcat(policy,u)

    peers=[r for r in get_peer_receipts() if verify_peer_receipt(r)]

    s["trust"]=decay(s.get("trust",{}))

    actions=[local]+[p.get("consensus_action","monitor") for p in peers]
    consensus=vote(actions) if quorum(peers) else local

    anomaly=detect_anomaly(s["u"])
    final,why=arbitrate(local,consensus,anomaly)

    receipt={
        "node":get_node_id(),
        "cycle":s["cycles"],
        "u":u,
        "local":local,
        "consensus":consensus,
        "final":final,
        "reason":why
    }

    receipt["hash"],receipt["signature"]=sign_with_keypair(receipt)

    os.makedirs("payload/receipts",exist_ok=True)
    json.dump(receipt,open(f"payload/receipts/r_{s['cycles']:04d}.json","w"),indent=2)

    record(receipt)
    save(s)

    print("SUMMARY:",receipt)

if __name__=="__main__":
    main()
