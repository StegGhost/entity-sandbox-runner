import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_FILE = ROOT / "brain_reports" / "repo_snapshot.json"


def run_step(cmd):
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT
        )
        duration = time.time() - start

        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "output": None,
            "raw_output": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "duration": round(duration, 3)
        }

    except Exception as e:
        return {
            "ok": False,
            "returncode": 1,
            "output": None,
            "raw_output": "",
            "stderr": str(e),
            "duration": 0
        }


def ensure_snapshot_exists():
    if SNAPSHOT_FILE.exists():
        return True
    return False


def main():
    loop_start = time.time()

    # -----------------
    # STEP 1: EXPLORE
    # -----------------
    explore = run_step(["python", "install/engine/repo_snapshot.py"])

    # HARD GUARANTEE: snapshot must exist
    if not ensure_snapshot_exists():
        explore["ok"] = False
        explore["stderr"] = "repo_snapshot_not_created"

    # -----------------
    # STEP 2: NEXT ACTION
    # -----------------
    next_action = run_step(["python", "install/engine/next_action_engine.py"])

    # Parse next_action JSON if possible
    action_payload = None
    try:
        if next_action["raw_output"]:
            action_payload = json.loads(next_action["raw_output"])
    except Exception:
        pass

    # -----------------
    # STEP 3: EXECUTE
    # -----------------
    execute = None

    action = None
    if action_payload:
        action = action_payload.get("next_action", {}).get("action")

    # HANDLE IDLE SAFELY
    if action == "idle":
        execute = {
            "ok": True,
            "returncode": 0,
            "output": {
                "status": "ok",
                "executed": False,
                "reason": "idle_no_op"
            },
            "raw_output": "",
            "stderr": "",
            "duration": 0.0
        }
    else:
        execute = run_step(["python", "install/engine/execute_next_action.py"])

    # -----------------
    # STEP 4: RECONCILE
    # -----------------
    reconcile = run_step(["python", "install/engine/reconcile_execution_state.py"])

    total_duration = round(time.time() - loop_start, 3)

    output = {
        "status": "ok",
        "mode": "closed_loop_autonomous",
        "loop_ok": True,
        "duration_seconds": total_duration,
        "steps": {
            "explore": explore,
            "next_action": next_action,
            "execute": execute,
            "reconcile": reconcile
        }
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
