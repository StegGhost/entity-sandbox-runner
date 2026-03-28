import json
import time
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"

POLICY_PATH = Path(__file__).parent / "policy.json"
OUTPUT = REPORTS / "tvc_token.json"


def load(path):
    try:
        return json.loads(path.read_text())
    except:
        return None


def now():
    return int(time.time())


def fail(reason):
    print(json.dumps({"status": "rejected", "reason": reason}, indent=2))
    raise SystemExit(0)


def main():
    policy = load(POLICY_PATH)
    reconcile = load(REPORTS / "reconcile_result.json")
    headless = load(REPORTS / "headless_cmd_test.json")

    if not policy:
        fail("missing_policy")

    rule = policy["rules"][0]

    if rule["require_reconcile_ok"]:
        if not reconcile or reconcile.get("status") != "ok":
            fail("reconcile_not_ok")

    if rule["require_headless_ok"]:
        if not headless or headless.get("status") != "ok":
            fail("headless_not_ok")

    payload = {
        "status": "issued",
        "ts": now(),
        "ttl": rule["ttl_seconds"],
        "scope": rule["scope"],
        "quorum_required": rule["require_quorum"],
        "quorum_min": rule["quorum_min"]
    }

    raw = json.dumps(payload, sort_keys=True).encode()
    payload["token"] = hashlib.sha256(raw).hexdigest()

    OUTPUT.write_text(json.dumps(payload, indent=2))

    print(json.dumps({
        "status": "ok",
        "output": str(OUTPUT)
    }, indent=2))


if __name__ == "__main__":
    main()
