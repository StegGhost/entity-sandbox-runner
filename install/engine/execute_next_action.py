import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"
EXECUTION_RESULT_PATH = BRAIN_REPORTS / "execute_next_action_result.json"

INCOMING_DIR = ROOT / "incoming_bundles"
FAILED_DIR = ROOT / "failed_bundles"
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


def resolve_target_bundle(target: str):
    if not target:
        return None

    target_path = Path(target)

    if target_path.is_absolute() and target_path.exists():
        return target_path

    repo_relative = ROOT / target_path
    if repo_relative.exists():
        return repo_relative

    incoming_candidate = INCOMING_DIR / target_path.name
    if incoming_candidate.exists():
        return incoming_candidate

    failed_candidate = FAILED_DIR / target_path.name
    if failed_candidate.exists():
        return failed_candidate

    repaired_candidate = REPAIRED_DIR / target_path.name
    if repaired_candidate.exists():
        return repaired_candidate

    return None


def inspect_incoming_bundle(target_path: str):
    src = resolve_target_bundle(target_path)

    if src is None or not src.exists():
        return {
            "status": "failed",
            "reason": "incoming_bundle_missing",
            "target": target_path,
        }

    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    dest = FAILED_DIR / src.name

    shutil.move(str(src), str(dest))

    return {
        "status": "ok",
        "action": "classified_to_failed",
        "bundle": str(dest),
    }


def handle_repair(next_action: dict):
    target = next_action.get("target")
    family = next_action.get("family")

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

    shutil.copy2(str(resolved), str(repaired_path))

    return {
        "status": "ok",
        "family": family,
        "original_bundle": str(resolved),
        "repaired_bundle": str(repaired_path),
        "ts": ts,
    }


def execute_action(next_action: dict | None):
    if not next_action:
        return {
            "status": "failed",
            "executed": False,
            "reason": "no_action",
        }

    action_type = next_action.get("action")

    if action_type == "idle":
        return {
            "status": "ok",
            "executed": False,
            "reason": "idle_no_op",
        }

    if action_type == "inspect_incoming_bundle_family":
        result = inspect_incoming_bundle(next_action.get("target"))
        return {
            "status": "ok",
            "executed": True,
            "execution": result,
        }

    if action_type == "propose_repair_for_bundle_family":
        result = handle_repair(next_action)
        return {
            "status": "ok",
            "executed": True,
            "execution": {
                "status": "ok",
                "action": "repair_bundle",
                "result": result,
            },
        }

    return {
        "status": "failed",
        "executed": False,
        "reason": f"unsupported_action:{action_type}",
    }


def main():
    wrapper = load_json(NEXT_ACTION_PATH)

    if not wrapper:
        payload = {
            "status": "failed",
            "executed": False,
            "reason": "missing_next_action",
            "timestamp": datetime.utcnow().isoformat(),
        }
        write_json(EXECUTION_RESULT_PATH, payload)
        print(json.dumps(payload, indent=2))
        return

    next_action = wrapper.get("next_action")
    result = execute_action(next_action)

    if "timestamp" not in result:
        result["timestamp"] = datetime.utcnow().isoformat()

    # Critical contract: reconcile reads this file
    write_json(EXECUTION_RESULT_PATH, result)

    # Optional sanity marker for easier debugging
    marker = {
        "written_at": datetime.utcnow().isoformat(),
        "execution_result_path": str(EXECUTION_RESULT_PATH),
        "exists": EXECUTION_RESULT_PATH.exists(),
    }
    write_json(BRAIN_REPORTS / "execute_write_check.json", marker)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
