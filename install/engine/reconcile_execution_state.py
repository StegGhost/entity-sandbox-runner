import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
EXECUTION_RESULT_PATH = BRAIN_REPORTS / "execute_next_action_result.json"
RECONCILED_STATE_PATH = BRAIN_REPORTS / "reconciled_state.json"


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def reconcile_execution_result(execution_result: dict | None) -> dict:
    if not execution_result:
        return {
            "status": "failed",
            "review_state": "failed",
            "reason": "missing_execution_result",
        }

    if execution_result.get("status") != "ok":
        return {
            "status": "failed",
            "review_state": "failed",
            "reason": execution_result.get("reason", "execution_not_ok"),
        }

    # Idle/no-op is admissible and stable
    if execution_result.get("executed") is False:
        return {
            "status": "ok",
            "review_state": "idle",
            "reason": execution_result.get("reason", "idle_no_op"),
        }

    execution = execution_result.get("execution")
    if not isinstance(execution, dict):
        return {
            "status": "failed",
            "review_state": "failed",
            "reason": "missing_execution_payload",
        }

    exec_status = execution.get("status")
    if exec_status != "ok":
        return {
            "status": "failed",
            "review_state": "failed",
            "reason": execution.get("reason", "execution_payload_not_ok"),
        }

    action = execution.get("action")

    # Incoming bundle classified into failed queue
    if action == "classified_to_failed":
        return {
            "status": "ok",
            "review_state": "classified",
            "bundle": execution.get("bundle"),
            "family": None,
        }

    # Repair path
    if action == "repair_bundle":
        result = execution.get("result", {})
        if result.get("status") == "ok":
            return {
                "status": "ok",
                "review_state": "repaired",
                "bundle": result.get("repaired_bundle"),
                "family": result.get("family"),
            }
        return {
            "status": "failed",
            "review_state": "failed",
            "reason": result.get("reason", "repair_result_not_ok"),
            "bundle": result.get("target") or result.get("original_bundle"),
            "family": result.get("family"),
        }

    # Generic executed-ok fallback
    return {
        "status": "ok",
        "review_state": "processed",
        "action": action,
    }


def main():
    execution_result = load_json(EXECUTION_RESULT_PATH)
    reconciled_state = reconcile_execution_result(execution_result)

    payload = {
        "status": "ok" if reconciled_state.get("status") == "ok" else "failed",
        "reconciled_state": reconciled_state,
    }

    write_json(RECONCILED_STATE_PATH, payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
