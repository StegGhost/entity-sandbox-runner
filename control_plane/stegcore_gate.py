import json
import time
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "brain_reports"


def load_json(name):
    path = REPORT_DIR / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def hash_decision(payload):
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


def evaluate():
    headless = load_json("headless_cmd_test.json")
    reconcile = load_json("reconcile_result.json")

    decision = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "unknown",
        "admissible": False,
        "checks": {},
        "reason": None
    }

    # --- CHECK 1: RECEIPT PRESENT ---
    receipt = headless.get("steps", {}).get("execute", {}).get("data", {}).get("receipt")
    decision["checks"]["receipt_present"] = receipt is not None

    # --- CHECK 2: POLICY PASSED ---
    policy_passed = receipt.get("policy_passed") if receipt else False
    decision["checks"]["policy_passed"] = policy_passed is True

    # --- CHECK 3: HASH BINDING ---
    binding = headless.get("binding", {})
    decision["checks"]["execution_bound"] = binding.get("match") is True

    # --- CHECK 4: RECONCILE OK ---
    decision["checks"]["reconcile_ok"] = reconcile.get("status") == "ok"

    # --- FINAL ADMISSIBILITY ---
    if all(decision["checks"].values()):
        decision["admissible"] = True
        decision["status"] = "approved"
        decision["reason"] = "all_constraints_satisfied"
    else:
        decision["admissible"] = False
        decision["status"] = "rejected"
        decision["reason"] = "constraint_violation"

    # --- DECISION HASH ---
    decision["decision_hash"] = hash_decision(decision)

    out = REPORT_DIR / "stegcore_gate_result.json"
    out.write_text(json.dumps(decision, indent=2), encoding="utf-8")

    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    evaluate()
