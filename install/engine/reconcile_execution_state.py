import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
BRAIN_REPORTS = ROOT / "brain_reports"
EXECUTION_RESULT_PATH = BRAIN_REPORTS / "execution_result.json"
RECONCILE_RESULT_PATH = BRAIN_REPORTS / "reconcile_result.json"


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


def main():
    execution_payload = load_json(EXECUTION_RESULT_PATH)

    if not execution_payload:
        result = {
            "status": "failed",
            "reason": "missing_execution_result",
            "output": str(RECONCILE_RESULT_PATH),
            "ts": datetime.utcnow().isoformat()
        }
        write_json(RECONCILE_RESULT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    execution_result = execution_payload.get("execution_result", {})

    if execution_payload.get("status") != "ok":
        result = {
            "status": "needs_retry",
            "reason": execution_result.get("error", execution_payload.get("reason", "execution_failed")),
            "output": str(RECONCILE_RESULT_PATH),
            "ts": datetime.utcnow().isoformat()
        }
        write_json(RECONCILE_RESULT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    if execution_payload.get("executed") is False:
        result = {
            "status": "idle",
            "reason": execution_payload.get("reason", "idle_no_op"),
            "output": str(RECONCILE_RESULT_PATH),
            "ts": datetime.utcnow().isoformat()
        }
        write_json(RECONCILE_RESULT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    receipt = execution_result.get("execution", {}).get("receipt")

    if not receipt:
        result = {
            "status": "invalid",
            "reason": "missing_receipt",
            "output": str(RECONCILE_RESULT_PATH),
            "ts": datetime.utcnow().isoformat()
        }
        write_json(RECONCILE_RESULT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    if not receipt.get("policy_passed"):
        result = {
            "status": "rejected",
            "reason": "policy_failed",
            "output": str(RECONCILE_RESULT_PATH),
            "ts": datetime.utcnow().isoformat()
        }
        write_json(RECONCILE_RESULT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    result = {
        "status": "committed",
        "receipt_id": receipt.get("receipt_id"),
        "target": receipt.get("target"),
        "output": str(RECONCILE_RESULT_PATH),
        "ts": datetime.utcnow().isoformat()
    }

    write_json(RECONCILE_RESULT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
