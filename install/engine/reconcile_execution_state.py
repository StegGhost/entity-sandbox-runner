import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXECUTION_RESULT_PATH = ROOT / "brain_reports" / "execute_next_action_result.json"


def load_execution_result():
    if not EXECUTION_RESULT_PATH.exists():
        return None

    try:
        return json.loads(EXECUTION_RESULT_PATH.read_text())
    except Exception:
        return None


def reconcile_state(execution_result: dict):
    if not execution_result:
        return {
            "status": "failed",
            "reason": "no_execution_result"
        }

    execution = execution_result.get("execution", {})
    result = execution.get("result", {})

    # 🔥 CRITICAL FIX: prefer repaired bundle if present
    repaired_bundle = result.get("repaired_bundle")
    original_bundle = result.get("original_bundle")

    bundle_used = repaired_bundle or original_bundle

    if execution.get("status") != "ok":
        return {
            "status": "failed",
            "review_state": "failed",
            "bundle": original_bundle,
            "reason": "execution_failed"
        }

    return {
        "status": "ok",
        "review_state": "repaired",
        "bundle": bundle_used,
        "family": result.get("family")
    }


def main():
    execution_result = load_execution_result()

    reconciled = reconcile_state(execution_result)

    output = {
        "status": "ok" if reconciled.get("status") == "ok" else "failed",
        "reconciled_state": reconciled
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
