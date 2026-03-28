import json
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAIN_REPORTS = ROOT / "brain_reports"

NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"
EXECUTION_RESULT_PATH = BRAIN_REPORTS / "execution_result.json"
RECONCILE_RESULT_PATH = BRAIN_REPORTS / "reconcile_result.json"
TRACE_PATH = BRAIN_REPORTS / "orchestrator_trace.json"
SUMMARY_PATH = BRAIN_REPORTS / "loop_summary.json"


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


def parse_json_maybe(text: str):
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def run_step(name: str, cmd: list[str]) -> dict:
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True
        )
        result = {
            "name": name,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "duration": round(time.time() - start, 3),
            "parsed_stdout": parse_json_maybe(proc.stdout.strip()),
        }
        return result
    except Exception as e:
        return {
            "name": name,
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": round(time.time() - start, 3),
            "parsed_stdout": None,
        }


def require_file_json(path: Path, name: str):
    payload = load_json(path)
    if payload is None:
        raise RuntimeError(f"{name}_missing:{path}")
    return payload


def main():
    trace = {
        "ts": now_ts(),
        "status": "running",
        "steps": []
    }

    summary = {
        "ts": now_ts(),
        "status": "invalid",
        "reason": None,
        "ingestion_ok": False,
        "next_action_ok": False,
        "execute_ok": False,
        "reconcile_ok": False,
        "next_action": None,
        "execution_reason": None,
        "reconcile_reason": None,
        "paths": {
            "next_action": str(NEXT_ACTION_PATH),
            "execution_result": str(EXECUTION_RESULT_PATH),
            "reconcile_result": str(RECONCILE_RESULT_PATH),
            "trace": str(TRACE_PATH),
            "summary": str(SUMMARY_PATH),
        },
    }

    try:
        ingestion = run_step("ingestion", ["python", "install/ingestion_v2.py"])
        trace["steps"].append(ingestion)
        summary["ingestion_ok"] = ingestion["ok"]

        next_action_step = run_step("next_action", ["python", "install/engine/next_action_engine.py"])
        trace["steps"].append(next_action_step)
        summary["next_action_ok"] = next_action_step["ok"]

        next_action_payload = require_file_json(NEXT_ACTION_PATH, "next_action")
        next_action = next_action_payload.get("next_action", {})
        summary["next_action"] = next_action

        execute_step = run_step("execute", ["python", "install/engine/execute_next_action.py"])
        trace["steps"].append(execute_step)
        summary["execute_ok"] = execute_step["ok"]

        execution_payload = require_file_json(EXECUTION_RESULT_PATH, "execution_result")
        execution_reason = execution_payload.get("reason")
        if execution_reason is None and isinstance(execution_payload.get("result"), dict):
            execution_reason = execution_payload["result"].get("reason")
        summary["execution_reason"] = execution_reason

        reconcile_step = run_step("reconcile", ["python", "install/engine/reconcile_execution_state.py"])
        trace["steps"].append(reconcile_step)
        summary["reconcile_ok"] = reconcile_step["ok"]

        reconcile_payload = require_file_json(RECONCILE_RESULT_PATH, "reconcile_result")
        summary["reconcile_reason"] = reconcile_payload.get("reason")

        next_action_name = None
        if isinstance(next_action, dict):
            next_action_name = next_action.get("action")

        reconcile_status = reconcile_payload.get("status")
        reconcile_reason = reconcile_payload.get("reason")

        lifecycle_ok = (
            reconcile_status == "ok"
            and reconcile_reason in {"receipt_present", "lifecycle_reconciled_without_receipt"}
        )

        if not ingestion["ok"]:
            raise RuntimeError("ingestion_failed")

        if not next_action_step["ok"]:
            raise RuntimeError("next_action_failed")

        if not execute_step["ok"]:
            raise RuntimeError("execute_failed")

        if not reconcile_step["ok"]:
            raise RuntimeError("reconcile_step_failed")

        if not lifecycle_ok:
            raise RuntimeError(f"reconcile_invalid:{reconcile_reason}")

        summary["status"] = "ok"
        summary["reason"] = "loop_hardened_path_passed"
        summary["action"] = next_action_name
        trace["status"] = "ok"

    except Exception as e:
        trace["status"] = "failed"
        trace["error"] = str(e)
        summary["status"] = "failed"
        summary["reason"] = str(e)

    write_json(TRACE_PATH, trace)
    write_json(SUMMARY_PATH, summary)

    print(json.dumps({
        "status": summary["status"],
        "output": str(SUMMARY_PATH),
        "summary": summary,
        "trace_output": str(TRACE_PATH),
    }, indent=2))

    if summary["status"] != "ok":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
