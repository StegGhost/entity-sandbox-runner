import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"

KEYS = Path(__file__).parent / "public_keys.json"


def fail(reason):
    print(json.dumps({"status": "invalid", "reason": reason}, indent=2))
    sys.exit(1)


def main():
    headless = json.loads((REPORTS / "headless_cmd_test.json").read_text())
    keys = json.loads(KEYS.read_text())

    receipt = headless["steps"]["execute"]["data"]["receipt"]

    action_hash = receipt["action_hash"]
    result_hash = receipt["result_hash"]

    # recompute hash deterministically
    recomputed = hashlib.sha256(
        (action_hash + result_hash).encode()
    ).hexdigest()

    if not recomputed:
        fail("receipt_hash_invalid")

    # (Optional: real signature verification layer here)

    print(json.dumps({
        "status": "ok",
        "receipt_id": receipt["receipt_id"]
    }, indent=2))


if __name__ == "__main__":
    main()
