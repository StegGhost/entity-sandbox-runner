import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"
EXECUTION_RESULT_PATH = BRAIN_REPORTS / "execute_next_action_result.json"

FAILED_DIR = ROOT / "failed_bundles"
INCOMING_DIR = ROOT / "incoming_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def resolve_target_bundle(target: str) -> Path | None:
    if not target:
        return None

    target_path = Path(target)

    # Absolute path
    if target_path.is_absolute() and target_path.exists():
        return target_path

    # Relative path from repo root
    repo_relative = ROOT / target_path
    if repo_relative.exists():
        return repo_relative

    # Fallback: failed_bundles/<filename>
    failed_candidate = FAILED_DIR / target_path.name
    if failed_candidate.exists():
        return failed_candidate

    # Fallback: incoming_bundles/<filename>
    incoming_candidate = INCOMING_DIR / target_path.name
    if incoming_candidate.exists():
        return incoming_candidate

    return None


def handle_repair(action: dict) -> dict:
    target = action.get("target")
    family = action.get("family")

    resolved = resolve_target_bundle(target)
    if resolved is None:
        return {
            "status": "failed",
            "reason": "bundle_not_found",
            "target": target,
            "family": family,
        }

    REPAIRED_DIR.mkdir(parents=True, exist_ok=True)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    repaired_name = f"{resolved.stem}_repaired_{ts}{resolved.suffix}"
    repaired_path = REPAIRED_DIR / repaired_name

    try:
        shutil.copy2(resolved, repaired_path)
    except Exception as exc:
        return {
            "status": "failed",
            "reason": f"copy_failed:{exc}",
            "target": str(resolved),
            "family": family,
        }

    return {
        "status": "ok",
        "family": family,
        "original_bundle": str(resolved),
        "repaired_bundle": str(repaired_path),
        "ts": ts,
    }


def execute_action(action: dict | None) -> dict:
    if not action:
        return {
            "status": "failed",
            "reason": "no_action",
        }

    action_type = action.get("action")

    if action_type == "propose_repair_for_bundle_family":
        return {
            "status": "ok",
            "action": "repair_bundle",
            "result": handle_repair(action),
        }

    return {
        "status": "failed",
        "reason": f"unsupported_action:{action_type}",
    }


def main():
    next_action_wrapper = load_json(NEXT_ACTION_PATH)

    if not next_action_wrapper:
        payload = {
            "status": "failed",
            "executed": False,
            "reason": "missing_next_action",
        }
        write_json(EXECUTION_RESULT_PATH, payload)
        print(json.dumps(payload, indent=2))
        return

    next_action = next_action_wrapper.get("next_action")
    execution = execute_action(next_action)

    payload = {
        "status": "ok",
        "executed": True,
        "timestamp": datetime.utcnow().isoformat(),
        "execution": execution,
    }

    write_json(EXECUTION_RESULT_PATH, payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
