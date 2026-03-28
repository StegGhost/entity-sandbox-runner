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


def extract_result_block(payload):
    if not isinstance(payload, dict):
        return None

    # Shape A:
    # {
    #   "status": "...",
    #   "output": "...",
    #   "result": { ... actual execution result ... }
    # }
    nested = payload.get("result")
    if isinstance(nested, dict):
        return nested

    # Shape B:
    # { ... actual execution result directly at top level ... }
    if "action" in payload or "reason" in payload or "worker_result" in payload:
        return payload

    return None


def extract_receipt(result_block):
    if not isinstance(result_block, dict):
        return None

    worker_result = result_block.get("worker_result")
    if isinstance(worker_result, dict):
        parsed = worker_result.get("parsed_stdout")
        if isinstance(parsed, dict):
            if isinstance(parsed.get("receipt"), dict):
                return parsed.get("receipt")

            data = parsed.get("data")
            if isinstance(data, dict) and isinstance(data.get("receipt"), dict):
                return data.get("receipt")

    return None


def main():
    execution_payload = load_json(EXECUTION_RESULT_PATH)
    if execution_payload is None:
        result = {
            "status": "invalid",
            "reason": "missing_execution_result",
            "action": None,
            "execution_reason": None,
            "output": str(OUTPUT_PATH),
            "ts": now_ts(),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    result_block = extract_result_block(execution_payload)
    if not isinstance(result_block, dict):
        result = {
            "status": "invalid",
            "reason": "invalid_execution_result_shape",
            "action": None,
            "execution_reason": None,
            "output": str(OUTPUT_PATH),
            "ts": now_ts(),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    action = result_block.get("action")
    execution_reason = result_block.get("reason")
    receipt = extract_receipt(result_block)

    if isinstance(receipt, dict):
        result = {
            "status": "ok",
            "reason": "receipt_present",
            "action": action,
            "execution_reason": execution_reason,
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

    lifecycle_reasons = {
        "repair_completed",
        "repair_completed_and_reintegrated",
        "inspection_completed",
        "reintegrate_completed",
        "promoted_to_install",
    }

    reintegrate_result = result_block.get("reintegrate_result")
    repair_result = result_block.get("repair_result")

    reintegrated_ok = False
    if isinstance(reintegrate_result, dict):
        if reintegrate_result.get("ok") is True:
            reintegrated_ok = True
        parsed_stdout = reintegrate_result.get("parsed_stdout")
        if isinstance(parsed_stdout, dict):
            nested_result = parsed_stdout.get("result")
            if isinstance(nested_result, dict) and nested_result.get("status") == "ok":
                reintegrated_ok = True

    if action in lifecycle_actions and execution_reason in lifecycle_reasons:
        result = {
            "status": "ok",
            "reason": "lifecycle_reconciled_without_receipt",
            "action": action,
            "execution_reason": execution_reason,
            "receipt_present": False,
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
        "execution_reason": execution_reason,
        "output": str(OUTPUT_PATH),
        "ts": now_ts(),
    }
    write_json(OUTPUT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
