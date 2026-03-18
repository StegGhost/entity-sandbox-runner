import json
import os
import random

from install.policy_engine import load_policy, normalize_policy, validate_remote_policy
from install.bcat_engine import enforce_bcat
from install.crypto_keys import sign_with_keypair, verify_chain
from install.replay import record_cycle
from install.remote_policy import fetch_remote_policy
from install.finco import apply_finco

STATE_FILE = "logs/state.json"
REMOTE_POLICY_URL = None  # set later when you have a trusted endpoint


def load_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "cycles": 0,
        "last_hash": None,
        "policy_events": [],
    }


def save_state(state):
    os.makedirs("logs", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def run_cycle():
    results = []
    for shard in ["s1", "s2", "s3"]:
        confidence = random.uniform(0.5, 0.9)
        decision = "ok" if confidence > 0.6 else "fail"
        results.append(
            {
                "shard": shard,
                "confidence": confidence,
                "decision": decision,
            }
        )
    return results


def compute_u(results):
    return sum(r["confidence"] for r in results) / len(results)


def prune_policy_events(state):
    state["policy_events"] = state.get("policy_events", [])[-50:]


def main():
    state = load_state()
    state["cycles"] += 1

    results = run_cycle()
    u = compute_u(results)

    # Start from trusted local policy
    policy = load_policy()
    policy_source = "local"
    policy_validation = "local_only"

    # Optionally merge remote policy, but only if it passes validation
    if REMOTE_POLICY_URL:
        remote = fetch_remote_policy(REMOTE_POLICY_URL)
        if remote is not None:
            if validate_remote_policy(remote):
                policy = normalize_policy(remote)
                policy_source = "remote"
                policy_validation = "accepted"
            else:
                policy_source = "local_fallback"
                policy_validation = "rejected_remote_policy"
                state.setdefault("policy_events", []).append(
                    {
                        "cycle": state["cycles"],
                        "event": "remote_policy_rejected",
                    }
                )

    # Simulated economic / external pressure
    external_signal = random.uniform(0.4, 0.8)
    u = apply_finco(u, external_signal)

    action, reason = enforce_bcat(policy, u)

    receipt = {
        "cycle": state["cycles"],
        "u": u,
        "action": action,
        "reason": reason,
        "external_signal": external_signal,
        "policy_source": policy_source,
        "policy_validation": policy_validation,
        "prev_hash": state.get("last_hash"),
    }

    receipt["hash"], receipt["signature"] = sign_with_keypair(receipt)

    os.makedirs("payload/receipts", exist_ok=True)
    receipt_path = f"payload/receipts/r_{state['cycles']:04d}.json"
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)

    verify_chain("payload/receipts")

    state["last_hash"] = receipt["hash"]
    prune_policy_events(state)
    save_state(state)

    record_cycle(state, results, action, u)

    print("SUMMARY:", receipt)


if __name__ == "__main__":
    main()
