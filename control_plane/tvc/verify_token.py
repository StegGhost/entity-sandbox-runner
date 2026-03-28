import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"

TOKEN_PATH = REPORTS / "tvc_token.json"


def fail(reason):
    print(json.dumps({
        "status": "invalid",
        "reason": reason
    }, indent=2))
    return False


def main():
    if not TOKEN_PATH.exists():
        return fail("missing_token")

    try:
        token = json.loads(TOKEN_PATH.read_text())
    except:
        return fail("invalid_json")

    if token.get("status") != "issued":
        return fail("not_issued")

    ts = token.get("ts")
    ttl = token.get("ttl", 0)

    if not ts or time.time() > ts + ttl:
        return fail("expired")

    print(json.dumps({
        "status": "valid",
        "scope": token.get("scope")
    }, indent=2))

    return True


if __name__ == "__main__":
    ok = main()
    if not ok:
        raise SystemExit(1)
