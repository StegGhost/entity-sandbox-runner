import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BRAIN_REPORTS = ROOT / "brain_reports"

EXECUTION_RESULT_PATH = BRAIN_REPORTS / "execution_result.json"
OUTPUT_PATH = BRAIN_REPORTS / "reconcile_result.json"


def now_ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, str):
            data = json.loads(data)
        return data
    except Exception:
        return None


def main():
    execution_payload = load_json(EXECUTION_RESULT_PATH)
    if not isinstance(execution_payload, dict):
        result = {
            "status": "invalid",
            "reason": "missing_execution_result",
            "output": str(OUTPUT_PATH),
            "ts": now_ts(),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    result_block = execution_payload.get("result", {})
    if not isinstance(result_block, dict):
        result = {
            "status": "invalid",
            "reason": "invalid_execution_result",
            "output": str(OUTPUT_PATH),
            "ts": now_ts(),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    action = result_block.get("action")
    reason = result_block.get("reason")

    reintegrate_result = result_block.get("reintegrate_result")
    repair_result = result_block.get("repair_result")
    worker_result = result_block.get("worker_result")

    receipt = None

    if isinstance(worker_result, dict):
        parsed = worker_result.get("parsed_stdout")
        if isinstance(parsed, dict):
            worker_data = parsed.get("data")
            if isinstance(worker_data, dict):
                receipt = worker_data.get("receipt")
            if receipt is None:
                receipt = parsed.get("receipt")

    if receipt is not None:
        result = {
            "status": "ok",
            "reason": "receipt_present",
            "receipt_present": True,
            "receipt": receipt,
            "output": str(OUTPUT_PATH),
            "ts": now_ts(),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    lifecycle_actions = {
        "propose_repair_for_bundle_family",
        "inspect_incoming_bundle_family",
        "reintegrate_repaired_bundle",
    }

    reintegrated_ok = (
        isinstance(reintegrate_result, dict)
        and reintegrate_result.get("ok") is True
    )

    if action in lifecycle_actions and reason in {
        "repair_completed",
        "repair_completed_and_reintegrated",
        "inspection_completed",
        "reintegrate_completed",
    }:
        result = {
            "status": "ok",
            "reason": "lifecycle_reconciled_without_receipt",
            "receipt_present": False,
            "action": action,
            "execution_reason": reason,
            "repair_present": isinstance(repair_result, dict),
            "reintegrated_ok": reintegrated_ok,
            "output": str(OUTPUT_PATH),
            "ts": now_ts(),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    result = {
        "status": "invalid",
        "reason": "missing_receipt",
        "action": action,
        "execution_reason": reason,
        "output": str(OUTPUT_PATH),
        "ts": now_ts(),
    }
    write_json(OUTPUT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
