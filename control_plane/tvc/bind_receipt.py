import json
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"

TOKEN_PATH = REPORTS / "tvc_token.json"
HEADLESS_PATH = REPORTS / "headless_cmd_test.json"


def load(path):
    try:
        return json.loads(path.read_text())
    except:
        return None


def fail(reason):
    print(json.dumps({"status": "invalid", "reason": reason}, indent=2))
    sys.exit(1)


def main():
    token = load(TOKEN_PATH)
    headless = load(HEADLESS_PATH)

    if not token:
        fail("missing_token")

    if not headless:
        fail("missing_headless")

    receipt = headless.get("steps", {}).get("execute", {}).get("data", {}).get("receipt")

    if not receipt:
        fail("missing_receipt")

    binding = {
        "token": token["token"],
        "receipt_id": receipt["receipt_id"],
        "action_hash": receipt["action_hash"],
        "result_hash": receipt["result_hash"]
    }

    raw = json.dumps(binding, sort_keys=True).encode()
    binding_hash = hashlib.sha256(raw).hexdigest()

    output = REPORTS / "tvc_receipt_binding.json"
    output.write_text(json.dumps({
        "status": "bound",
        "binding_hash": binding_hash,
        "details": binding
    }, indent=2))

    print(json.dumps({
        "status": "ok",
        "output": str(output)
    }, indent=2))


if __name__ == "__main__":
    main()
