import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "brain_reports"

TOKEN_PATH = REPORTS / "tvc_token.json"
QUORUM_PATH = Path(__file__).parent / "quorum_signals.json"


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
    quorum = load(QUORUM_PATH)

    if not token:
        fail("missing_token")

    if not token.get("quorum_required"):
        print(json.dumps({"status": "ok", "reason": "no_quorum_required"}, indent=2))
        return

    signals = quorum.get("signals", [])
    approvals = [s for s in signals if s.get("approved")]

    if len(approvals) < token.get("quorum_min", 1):
        fail("quorum_not_met")

    print(json.dumps({
        "status": "ok",
        "approvals": len(approvals)
    }, indent=2))


if __name__ == "__main__":
    main()
