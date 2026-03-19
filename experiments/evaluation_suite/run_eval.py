import json, os, random

from install.rigel_invariant import compute_u
from install.rigel_policy import decide
from install.rigel_guard import enforce_delta_guard
from install.receipt_chain import build_receipt

STATE_FILE = "logs/state.json"


def load():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {"cycles": 0, "last_hash": None, "state": {}}


def save(s):
    os.makedirs("logs", exist_ok=True)
    json.dump(s, open(STATE_FILE, "w"), indent=2)


def simulate_components():
    return {
        "stability": random.uniform(0.6, 0.95),
        "trust": random.uniform(0.5, 0.9),
        "constraint_pressure": random.uniform(0.1, 0.6),
        "history": 1.0
    }


def main():
    s = load()
    s["cycles"] += 1

    prev_state = s.get("state", {})

    components = simulate_components()

    U = compute_u(components)

    allowed, norm, det, unc = enforce_delta_guard(prev_state, components)

    policy = {
        "hard_stop_u": 0.3,
        "restrict_u": 0.6
    }

    action, reason = decide(U, policy)

    if not allowed:
        action = "restrict"
        reason = f"uncertainty too high ({norm})"

    receipt = build_receipt(s.get("last_hash"), {
        "cycle": s["cycles"],
        "U": U,
        "action": action,
        "reason": reason,
        "delta_uncertainty": norm
    })

    os.makedirs("payload/receipts", exist_ok=True)
    json.dump(receipt, open(f"payload/receipts/r_{s['cycles']:04d}.json", "w"), indent=2)

    s["last_hash"] = receipt["hash"]
    s["state"] = components

    save(s)

    print("SUMMARY:", receipt)


if __name__ == "__main__":
    main()
