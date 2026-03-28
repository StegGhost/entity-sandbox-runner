import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"
OUTPUT_PATH = BRAIN_REPORTS / "execution_result.json"
HEADLESS_OUTPUT_PATH = BRAIN_REPORTS / "headless_cmd_test.json"

FAILED_DIR = ROOT / "failed_bundles"
INCOMING_DIR = ROOT / "incoming_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"


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
            "parsed_stdout": parse_json_maybe(proc.stdout.strip()),
        }
    except Exception as e:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": round(time.time() - start, 3),
            "parsed_stdout": None,
        }


def ensure_headless_artifact():
    if HEADLESS_OUTPUT_PATH.exists():
        return

    step = run_step([
        "python",
        "install/engine/headless_cmd_tester.py",
        "--mode",
        "steggate_live_test",
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
        },
    }
    write_json(HEADLESS_OUTPUT_PATH, fallback)


def resolve_bundle_path(target: str):
    if not target:
        return None

    p = Path(target)
    if p.exists():
        return p.resolve()

    candidates = [
        FAILED_DIR / target,
        INCOMING_DIR / target,
        REPAIRED_DIR / target,
    ]

    for c in candidates:
        if c.exists():
            return c.resolve()

    return None


def execute_repair_target(action: dict):
    target_from_action = action.get("target") or ""
    resolved_path = resolve_bundle_path(target_from_action)

    if not resolved_path:
        return {
            "status": "failed",
            "ts": now_ts(),
            "action": action.get("action"),
            "family": action.get("family"),
            "target": target_from_action,
            "resolved_path": None,
            "worker_result": None,
            "reintegrate_result": None,
            "reason": "missing_target",
        }

    worker_step = run_step([
        "python",
        "install/engine/repair_bundle.py",
        "--target",
        str(resolved_path),
    ])

    worker_payload = worker_step.get("parsed_stdout") or {}
    repair_result = worker_payload.get("result", {}) if isinstance(worker_payload, dict) else {}
    repaired_bundle = repair_result.get("output_bundle")

    reintegrate_step = None
    reintegrate_payload = None
    reintegrate_result = None

    if repaired_bundle:
        reintegrate_payload = {
            "repaired_bundle": repaired_bundle,
            "family": repair_result.get("family", action.get("family")),
            "original_bundle": str(resolved_path),
        }

        reintegrate_step = run_step([
            "python",
            "install/engine/reintegrate_repaired_bundle.py",
            "--action-payload-json",
            json.dumps(reintegrate_payload),
        ])

        reintegrate_stdout = reintegrate_step.get("parsed_stdout") or {}
        reintegrate_result = reintegrate_stdout.get("result", {}) if isinstance(reintegrate_stdout, dict) else None

    final_status = "ok" if worker_step["ok"] else "failed"
    final_reason = "repair_completed"

    if worker_step["ok"] and repaired_bundle and reintegrate_step is not None:
        final_status = "ok" if reintegrate_step["ok"] else "failed"
        final_reason = "repair_completed_and_reintegrated" if reintegrate_step["ok"] else "repair_completed_but_reintegration_failed"

    return {
        "status": final_status,
        "ts": now_ts(),
        "action": action.get("action"),
        "family": repair_result.get("family", action.get("family")),
        "target": target_from_action,
        "resolved_path": str(resolved_path),
        "worker_result": worker_step,
        "reintegrate_payload": reintegrate_payload,
        "reintegrate_result": reintegrate_step,
        "repair_result": repair_result,
        "reason": final_reason,
    }


def execute_inspection(action: dict):
    target = action.get("target", "")
    resolved_path = resolve_bundle_path(target)

    if not resolved_path:
        return {
            "status": "failed",
            "ts": now_ts(),
            "action": action.get("action"),
            "target": target,
            "resolved_path": None,
            "worker_result": None,
            "reason": "missing_target",
        }

    inspect_step = run_step([
        "python",
        "install/engine/inspect_bundle_engine.py",
        "--action-payload-json",
        json.dumps({
            **action,
            "target": str(resolved_path),
        }),
    ])

    return {
        "status": "ok" if inspect_step["ok"] else "failed",
        "ts": now_ts(),
        "action": action.get("action"),
        "target": str(resolved_path),
        "resolved_path": str(resolved_path),
        "worker_result": inspect_step,
        "reason": "inspection_completed" if inspect_step["ok"] else "inspection_failed",
    }


def execute_reintegrate(action: dict):
    target = action.get("target", "")
    resolved_path = resolve_bundle_path(target)

    if not resolved_path:
        return {
            "status": "failed",
            "ts": now_ts(),
            "action": action.get("action"),
            "target": target,
            "resolved_path": None,
            "worker_result": None,
            "reason": "missing_target",
        }

    reintegrate_step = run_step([
        "python",
        "install/engine/reintegrate_repaired_bundle.py",
        "--action-payload-json",
        json.dumps({
            **action,
            "target": str(resolved_path),
        }),
    ])

    return {
        "status": "ok" if reintegrate_step["ok"] else "failed",
        "ts": now_ts(),
        "action": action.get("action"),
        "target": str(resolved_path),
        "resolved_path": str(resolved_path),
        "worker_result": reintegrate_step,
        "reason": "reintegrate_completed" if reintegrate_step["ok"] else "reintegrate_failed",
    }


def main():
    payload = load_json(NEXT_ACTION_PATH)
    if not isinstance(payload, dict):
        ensure_headless_artifact()
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
        ensure_headless_artifact()
        result = {
            "status": "failed",
            "ts": now_ts(),
            "reason": "invalid_next_action_payload",
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": "failed", "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    action_name = action.get("action", "idle")

    if action_name == "idle":
        ensure_headless_artifact()
        result = {
            "status": "idle",
            "ts": now_ts(),
            "reason": "idle_no_op",
            "action": action_name,
            "target": action.get("target", ""),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": "idle", "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    if action_name == "propose_repair_for_bundle_family":
        result = execute_repair_target(action)
        ensure_headless_artifact()
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": result["status"], "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    if action_name == "inspect_incoming_bundle_family":
        result = execute_inspection(action)
        ensure_headless_artifact()
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": result["status"], "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    if action_name == "reintegrate_repaired_bundle":
        result = execute_reintegrate(action)
        ensure_headless_artifact()
        write_json(OUTPUT_PATH, result)
        print(json.dumps({"status": result["status"], "output": str(OUTPUT_PATH), "result": result}, indent=2))
        return

    ensure_headless_artifact()
    result = {
        "status": "failed",
        "ts": now_ts(),
        "reason": "unknown_action",
        "action": action_name,
        "target": action.get("target", ""),
    }
    write_json(OUTPUT_PATH, result)
    print(json.dumps({"status": "failed", "output": str(OUTPUT_PATH), "result": result}, indent=2))


if __name__ == "__main__":
    main()
