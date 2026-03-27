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


def reconcile_state(data: dict):
    if not data:
        return {
            "status": "failed",
            "reason": "no_execution_result"
        }

    # 🔥 handle actual structure correctly
    execution = data.get("execution", {})
    result = execution.get("result", {})

    if not execution or not result:
        return {
            "status": "failed",
            "review_state": "failed",
            "reason": "missing_execution_result"
        }

    if execution.get("status") != "ok":
        return {
            "status": "failed",
            "review_state": "failed",
            "reason": "execution_failed"
        }

    repaired_bundle = result.get("repaired_bundle")
    original_bundle = result.get("original_bundle")
    family = result.get("family")

    bundle_used = repaired_bundle or original_bundle

    return {
        "status": "ok",
        "review_state": "repaired" if repaired_bundle else "passed",
        "bundle": bundle_used,
        "family": family
    }


def main():
    data = load_execution_result()

    reconciled = reconcile_state(data)

    output = {
        "status": "ok" if reconciled.get("status") == "ok" else "failed",
        "reconciled_state": reconciled
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
