import json
import os
import random

from install.policy_engine import load_policy, normalize_policy, validate_remote_policy
from install.bcat_engine import enforce_bcat
from install.crypto_keys import sign_with_keypair, verify_chain
from install.replay import record_cycle
from install.remote_policy import fetch_remote_policy
from install.policy_signature import verify_remote_policy_signature
from install.finco import apply_finco
from install.node_consensus import compute_node_decision
from install.control_plane import load_control_plane_override

STATE_FILE = "logs/state.json"
REMOTE_POLICY_URL = None
REMOTE_POLICY_SIGNATURE_REQUIRED = True

def load_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"cycles": 0, "last_hash": None, "policy_events": [], "node_events": []}

def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def run_cycle():
    results = []
    for shard in ["s1", "s2", "s3"]:
        confidence = random.uniform(0.5, 0.9)
        decision = "ok" if confidence > 0.6 else "fail"
        results.append({"shard": shard, "confidence": confidence, "decision": decision})
    return results

def compute_u(results):
    return sum(r["confidence"] for r in results) / len(results)

def prune_events(state):
    state["policy_events"] = state.get("policy_events", [])[-50:]
    state["node_events"] = state.get("node_events", [])[-50:]

def main():
    state = load_state()
    state["cycles"] += 1

    results = run_cycle()
    u = compute_u(results)

    policy = load_policy()
    policy_source = "local"
    policy_validation = "local_only"

    if REMOTE_POLICY_URL:
        remote = fetch_remote_policy(REMOTE_POLICY_URL)
        if remote is not None:
            sig_ok = verify_remote_policy_signature(remote)
            schema_ok = validate_remote_policy(remote)
            if schema_ok and (sig_ok or not REMOTE_POLICY_SIGNATURE_REQUIRED):
                policy = normalize_policy(remote)
                policy_source = "remote"
                policy_validation = "accepted_signed_remote" if sig_ok else "accepted_unsigned_remote"
            else:
                policy_source = "local_fallback"
                policy_validation = "rejected_remote_policy"
                state.setdefault("policy_events", []).append({
                    "cycle": state["cycles"],
                    "event": "remote_policy_rejected",
                    "signature_ok": sig_ok,
                    "schema_ok": schema_ok,
                })

    external_signal = random.uniform(0.4, 0.8)
    u = apply_finco(u, external_signal)

    action, reason = enforce_bcat(policy, u)

    override = load_control_plane_override()
    override_applied = False
    if override and override.get("enabled") is True:
        forced_action = override.get("force_action")
        if forced_action in {"allow", "monitor", "restrict"}:
            action = forced_action
            reason = "control_plane_override"
            override_applied = True

    node_decision = compute_node_decision(action=action, u_signal=u)
    state.setdefault("node_events", []).append({
        "cycle": state["cycles"],
        "node_decision": node_decision,
    })

    receipt = {
        "cycle": state["cycles"],
        "u": u,
        "action": action,
        "reason": reason,
        "external_signal": external_signal,
        "policy_source": policy_source,
        "policy_validation": policy_validation,
        "override_applied": override_applied,
        "node_decision": node_decision,
        "prev_hash": state.get("last_hash"),
    }

    receipt["hash"], receipt["signature"] = sign_with_keypair(receipt)

    os.makedirs("payload/receipts", exist_ok=True)
    receipt_path = f"payload/receipts/r_{state['cycles']:04d}.json"
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    verify_chain("payload/receipts")

    state["last_hash"] = receipt["hash"]
    prune_events(state)
    save_state(state)

    record_cycle(state, results, action, u)

    print("SUMMARY:", receipt)

if __name__ == "__main__":
    main()
