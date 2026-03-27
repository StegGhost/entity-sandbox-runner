import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NEXT_ACTION_PATH = ROOT / "brain_reports" / "next_action.json"


def load_next_action():
    if not NEXT_ACTION_PATH.exists():
        return None
    try:
        return json.loads(NEXT_ACTION_PATH.read_text())
    except Exception:
        return None


def main():
    payload = load_next_action()

    if not payload:
        print(json.dumps({
            "status": "failed",
            "reason": "missing_next_action"
        }))
        return

    action = payload.get("next_action", {}).get("action")

    # ✅ SUPPORT IDLE
    if action == "idle":
        print(json.dumps({
            "status": "ok",
            "executed": False,
            "reason": "idle_no_op"
        }))
        return

    # existing logic continues here...
    print(json.dumps({
        "status": "failed",
        "reason": f"unsupported_action:{action}"
    }))
    

if __name__ == "__main__":
    main()
