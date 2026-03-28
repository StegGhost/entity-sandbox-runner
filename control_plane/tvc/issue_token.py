import json
import time
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"

OUTPUT = REPORTS / "tvc_token.json"


def now():
    return int(time.time())


def main():
    payload = {
        "status": "issued",
        "ts": now(),
        "ttl": 60,
        "scope": "promotion_to_main"
    }

    raw = json.dumps(payload, sort_keys=True).encode()
    token = hashlib.sha256(raw).hexdigest()

    payload["token"] = token

    OUTPUT.write_text(json.dumps(payload, indent=2))

    print(json.dumps({
        "status": "ok",
        "output": str(OUTPUT),
        "token": token
    }, indent=2))


if __name__ == "__main__":
    main()
