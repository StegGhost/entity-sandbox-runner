import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NEXT_ACTION_PATH = ROOT / "brain_reports" / "next_action.json"
INCOMING_DIR = ROOT / "incoming_bundles"
FAILED_DIR = ROOT / "failed_bundles"


def load_next_action():
    if not NEXT_ACTION_PATH.exists():
        return None
    try:
        return json.loads(NEXT_ACTION_PATH.read_text())
    except Exception:
        return None


def inspect_incoming_bundle(target_path):
    src = Path(target_path)

    if not src.exists():
        return {
            "status": "failed",
            "reason": "incoming_bundle_missing"
        }

    # MOVE → failed for now (safe deterministic behavior)
    dest = FAILED_DIR / src.name
    dest.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(src), str(dest))

    return {
        "status": "ok",
        "action": "classified_to_failed",
        "bundle": str(dest)
    }


def main():
    payload = load_next_action()

    if not payload:
        print(json.dumps({
            "status": "failed",
            "reason": "missing_next_action"
        }))
        return

    action = payload.get("next_action", {}).get("action")
    target = payload.get("next_action", {}).get("target")

    # ✅ IDLE
    if action == "idle":
        print(json.dumps({
            "status": "ok",
            "executed": False,
            "reason": "idle_no_op"
        }))
        return

    # ✅ INCOMING INSPECTION
    if action == "inspect_incoming_bundle_family":
        result = inspect_incoming_bundle(target)

        print(json.dumps({
            "status": "ok",
            "executed": True,
            "execution": result
        }))
        return

    # fallback
    print(json.dumps({
        "status": "failed",
        "reason": f"unsupported_action:{action}"
    }))


if __name__ == "__main__":
    main()
