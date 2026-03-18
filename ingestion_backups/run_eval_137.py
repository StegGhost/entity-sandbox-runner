
import json, os, random

from install.policy_engine import load_policy
from install.bcat_engine import enforce_bcat
from install.crypto_keys import sign_with_keypair, verify_chain
from install.replay import record_cycle
from install.network_registry import get_peer_receipts
from install.consensus_engine import weighted_consensus
from install.trust_engine import update_trust_scores
from install.adversarial_filter import filter_adversarial
from install.stability import compute_stability
from install.escalation import escalation_layer

STATE_FILE = "logs/state.json"

def load_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        return json.load(open(STATE_FILE))
    return {"cycles":0,"last_hash":None,"u_history":[]}

def save_state(state):
    os.makedirs("logs", exist_ok=True)
    json.dump(state, open(STATE_FILE,"w"), indent=2)

def run_cycle():
    return [{"confidence": random.uniform(0.5,0.9)} for _ in range(3)]

def compute_u(results):
    return sum(r["confidence"] for r in results)/len(results)

def main():
    state = load_state()
    state["cycles"] += 1

    results = run_cycle()
    u = compute_u(results)

    state["u_history"].append(u)
    state["u_history"] = state["u_history"][-20:]

    policy = load_policy()

    local_action, reason = enforce_bcat(policy, u)

    peers = get_peer_receipts()

    trust_scores = update_trust_scores(state, peers)
    filtered_peers = filter_adversarial(peers, trust_scores)

    consensus_action = weighted_consensus(local_action, filtered_peers)

    stability = compute_stability(state["u_history"])

    escalated_action, esc_reason = escalation_layer(u, stability)
    if escalated_action:
        consensus_action = escalated_action
        reason = esc_reason

    receipt = {
        "cycle": state["cycles"],
        "u": u,
        "local_action": local_action,
        "consensus_action": consensus_action,
        "stability": stability,
        "peers_seen": len(peers),
        "peers_used": len(filtered_peers),
        "prev_hash": state.get("last_hash")
    }

    receipt["hash"], receipt["signature"] = sign_with_keypair(receipt)

    os.makedirs("payload/receipts", exist_ok=True)
    path = f"payload/receipts/r_{state['cycles']:04d}.json"
    json.dump(receipt, open(path,"w"), indent=2)

    verify_chain("payload/receipts")

    state["last_hash"] = receipt["hash"]
    save_state(state)

    record_cycle(state, results, consensus_action, u)

    print("SUMMARY:", receipt)

if __name__ == "__main__":
    main()
