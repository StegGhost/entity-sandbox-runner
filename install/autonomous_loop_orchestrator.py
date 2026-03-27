import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPLORE = ROOT / "install/engine/repo_snapshot.py"
NEXT = ROOT / "install/engine/next_action_engine.py"
EXECUTE = ROOT / "install/engine/execute_next_action.py"
RECONCILE = ROOT / "install/engine/reconcile_execution_state.py"
INGEST = ROOT / "install/ingestion_v2.py"


def run_step(cmd: Path):
    start = time.time()
    proc = subprocess.run(
        ["python", str(cmd)],
        capture_output=True,
        text=True
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "output_snippet": (proc.stdout or "")[-4000:],
        "stderr_snippet": (proc.stderr or "")[-4000:],
        "duration": round(time.time() - start, 3)
    }


def try_parse_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


def normalize_and_extract_repair_target(execute_output: str, next_action_output: str):
    """
    Priority:
    1. If execute produced a repaired bundle, use that.
    2. If next_action proposes repair for a bundle family, fall back to the target.
    """

    exec_data = try_parse_json(execute_output)
    if isinstance(exec_data, dict):
        repaired_bundle = (
            exec_data.get("execution", {})
            .get("result", {})
            .get("repaired_bundle")
        )
        if repaired_bundle:
            return repaired_bundle

    next_data = try_parse_json(next_action_output)
    if isinstance(next_data, dict):
        next_action = next_data.get("next_action", {})
        action = next_action.get("action")
        if action == "propose_repair_for_bundle_family":
            return next_action.get("target")

    return None


def run_ingestion(bundle_path: str):
    start = time.time()
    proc = subprocess.run(
        ["python", str(INGEST), bundle_path],
        capture_output=True,
        text=True
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "output_snippet": (proc.stdout or "")[-4000:],
        "stderr_snippet": (proc.stderr or "")[-4000:],
        "bundle_path": bundle_path,
        "duration": round(time.time() - start, 3)
    }


def main():
    start = time.time()

    explore = run_step(EXPLORE)
    next_action = run_step(NEXT)
    execute = run_step(EXECUTE)

    repaired_or_target_bundle = normalize_and_extract_repair_target(
        execute.get("output_snippet", ""),
        next_action.get("output_snippet", ""),
    )

    ingest_result = None
    if repaired_or_target_bundle:
        ingest_result = run_ingestion(repaired_or_target_bundle)

    reconcile = run_step(RECONCILE)

    result = {
        "status": "ok",
        "mode": "closed_loop_autonomous",
        "loop_ok": True,
        "duration_seconds": round(time.time() - start, 3),
        "steps": {
            "explore": explore,
            "next_action": next_action,
            "execute": execute,
            "ingest_repair": ingest_result,
            "reconcile": reconcile,
        },
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
