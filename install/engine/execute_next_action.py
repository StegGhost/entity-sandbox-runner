import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"
OUTPUT_PATH = BRAIN_REPORTS / "execution_result.json"
HEADLESS_OUTPUT_PATH = BRAIN_REPORTS / "headless_cmd_test.json"


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


def run_step(cmd: list[str]):
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "duration": round(time.time() - start, 3),
        }
    except Exception as e:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": round(time.time() - start, 3),
        }


def ensure_headless_artifact():
    if HEADLESS_OUTPUT_PATH.exists():
        return

    step = run_step([
        "python",
        "install/engine/headless_cmd_tester.py",
        "--mode",
        "steggate_live_test"
    ])

    if HEADLESS_OUTPUT_PATH.exists():
        return

    fallback = {
        "mode": "steggate_live_test",
        "ts": now_ts(),
        "status": "failed",
        "reason": "headless_cmd_tester_did_not_emit_report",
        "generator_step": step,
        "steps": {
            "health": {"ok": False},
            "token": {"ok": False},
            "execute": {"ok": False},
            "verify": {"ok": False},
        }
    }
    write_json(HEADLESS_OUTPUT_PATH, fallback)


def main():
    payload = load_json(NEXT_ACTION_PATH)
    if not isinstance(payload, dict):
        result = {
            "status": "failed",
            "ts": now_ts(),
            "reason": "missing_next_action",
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": "failed", "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    action = payload.get("next_action", {})
    if not isinstance(action, dict):
        result = {
            "status": "failed",
            "ts": now_ts(),
            "reason": "invalid_next_action_payload",
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": "failed", "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    action_name = action.get("action")
    target = action.get("target", "")

    if action_name == "idle":
        ensure_headless_artifact()
        result = {
            "status": "idle",
            "ts": now_ts(),
            "reason": "idle_no_op",
            "action": action_name,
            "target": target,
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": "idle", "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    if not target:
        ensure_headless_artifact()
        result = {
            "status": "failed",
            "ts": now_ts(),
            "reason": "missing_target",
            "action": action_name,
            "target": target,
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": "failed", "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    target_path = Path(target)
    if not target_path.exists():
        ensure_headless_artifact()
        result = {
            "status": "failed",
            "ts": now_ts(),
            "reason": "target_not_found",
            "action": action_name,
            "target": target,
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": "failed", "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    if action_name == "propose_repair_for_bundle_family":
        step = run_step([
            "python",
            "install/engine/repair_bundle_engine.py",
            "--action-payload-json",
            json.dumps(action)
        ])
        ensure_headless_artifact()
        result = {
            "status": "ok" if step["ok"] else "failed",
            "ts": now_ts(),
            "action": action_name,
            "target": target,
            "worker_result": step,
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": result["status"], "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    if action_name == "reintegrate_repaired_bundle":
        step = run_step([
            "python",
            "install/engine/reintegrate_repaired_bundle.py",
            "--action-payload-json",
            json.dumps(action)
        ])
        ensure_headless_artifact()
        result = {
            "status": "ok" if step["ok"] else "failed",
            "ts": now_ts(),
            "action": action_name,
            "target": target,
            "worker_result": step,
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": result["status"], "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    if action_name == "inspect_incoming_bundle_family":
        step = run_step([
            "python",
            "install/engine/inspect_bundle_engine.py",
            "--action-payload-json",
            json.dumps(action)
        ])
        ensure_headless_artifact()
        result = {
            "status": "ok" if step["ok"] else "failed",
            "ts": now_ts(),
            "action": action_name,
            "target": target,
            "worker_result": step,
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": result["status"], "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    ensure_headless_artifact()
    result = {
        "status": "failed",
        "ts": now_ts(),
        "reason": "unknown_action",
        "action": action_name,
        "target": target,
    }
    write_json(OUTPUT_PATH, result)
    print(json.dumps({"status": "failed", "output": str(OUTPUT_PATH), "result": result}, indent=2))


if __name__ == "__main__":
    main()
