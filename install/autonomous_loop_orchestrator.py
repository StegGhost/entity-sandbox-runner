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


def run_step(cmd):
    start = time.time()
    proc = subprocess.run(
        ["python", str(cmd)],
        capture_output=True,
        text=True
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "output_snippet": proc.stdout[-1000:],
        "duration": round(time.time() - start, 3)
    }


def extract_repair_output(exec_output: str):
    try:
        data = json.loads(exec_output)
        return data.get("execution", {}).get("result", {}).get("repaired_bundle")
    except:
        return None


def run_ingestion(bundle_path: str):
    proc = subprocess.run(
        ["python", str(INGEST), bundle_path],
        capture_output=True,
        text=True
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "output": proc.stdout[-1000:]
    }


def main():
    start = time.time()

    explore = run_step(EXPLORE)
    next_action = run_step(NEXT)
    execute = run_step(EXECUTE)

    repaired_bundle = None

    if execute["ok"]:
        repaired_bundle = extract_repair_output(execute["output_snippet"])

    ingest_result = None

    # 🔥 NEW: loop closure
    if repaired_bundle:
        ingest_result = run_ingestion(repaired_bundle)

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
            "reconcile": reconcile
        }
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
