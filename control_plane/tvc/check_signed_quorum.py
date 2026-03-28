import json
import sys
from pathlib import Path
from crypto_utils import verify_signature

FILE = Path(__file__).parent / "signed_quorum.json"


def fail(reason):
    print(json.dumps({"status": "invalid", "reason": reason}, indent=2))
    sys.exit(1)


def main():
    data = json.loads(FILE.read_text())

    payload = data.get("payload")
    sigs = data.get("signatures", [])

    valid = 0

    for s in sigs:
        if verify_signature(s["signer"], payload, s["signature"]):
            valid += 1

    if valid < 2:
        fail("signed_quorum_not_met")

    print(json.dumps({
        "status": "ok",
        "valid_signatures": valid
    }, indent=2))


if __name__ == "__main__":
    main()
