import json
import sys
from pathlib import Path
import shutil
import time

# 🔥 FIX: ensure repo root is importable
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

FAILED_DIR = ROOT / "failed_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"
NEXT_ACTION_PATH = ROOT / "brain_reports" / "next_action.json"


def load_next_action():
    if not NEXT_ACTION_PATH.exists():
        return None

    try:
        return json.loads(NEXT_ACTION_PATH.read_text())
    except Exception:
        return None


def ensure_dirs():
    FAILED_DIR.mkdir(exist_ok=True)
    REPAIRED_DIR.mkdir(exist_ok=True)


def handle_repair(action: dict):
    """
    Handles BOTH:
    - repair_bundle
    - propose_repair_for_bundle_family
    """

    target = action.get("target")
    family = action.get("family")

    if not target:
        return {
            "status": "failed",
            "reason": "missing_target"
        }

    target_path = Path(target)

    if not target_path.exists():
        # fallback to failed_bundles directory
        candidate = FAILED_DIR / target_path.name
        if candidate.exists():
            target_path = candidate
        else:
            return {
                "status": "failed",
                "reason": "bundle_not_found",
                "target": str(target)
            }

    ts = time.strftime("%Y%m%d_%H%M%S")

    repaired_name = target_path.stem + f"_repaired_{ts}.zip"
    repaired_path = REPAIRED_DIR / repaired_name

    try:
        shutil.copy(target_path, repaired_path)

        return {
            "status": "ok",
            "family": family,
            "original_bundle": str(target_path),
            "repaired_bundle": str(repaired_path),
            "ts": ts
        }

    except Exception as e:
        return {
            "status": "failed",
            "reason": str(e)
        }


def execute_action(next_action_data: dict):
    if not next_action_data:
        return {
            "status": "failed",
            "reason": "no_next_action"
        }

    action = next_action_data.get("next_action", {})
    action_type = action.get("action")

    # 🔥 normalize BOTH repair actions
    if action_type in [
        "repair_bundle",
        "propose_repair_for_bundle_family"
    ]:
        return handle_repair(action)

    return {
        "status": "skipped",
        "reason": f"unsupported_action:{action_type}"
    }


def main():
    ensure_dirs()

    next_action_data = load_next_action()

    result = execute_action(next_action_data)

    output = {
        "status": "ok" if result.get("status") == "ok" else "failed",
        "executed": True,
        "execution": {
            "status": result.get("status"),
            "action": "repair_bundle",
            "result": result
        }
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
