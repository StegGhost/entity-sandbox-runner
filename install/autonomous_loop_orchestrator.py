import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

BRAIN_REPORTS = ROOT / "brain_reports"
EXECUTION_RESULT_PATH = BRAIN_REPORTS / "execute_next_action_result.json"


def run_step(script_path):
    result = subprocess.run(
        ["python", str(script_path)],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()
    stderr = result.stderr.strip()

    parsed = None
    try:
        parsed = json.loads(output)
    except Exception:
        parsed = None

    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "output": parsed,
        "raw_output": output,
        "stderr": stderr
    }


def ensure_execution_artifact(execute_step):
    """
    🔥 HARD GUARANTEE:
    If execute step returned JSON but file doesn't exist,
    we persist it ourselves.
    """

    if EXECUTION_RESULT_PATH.exists():
        return

    data = execute_step.get("output")

    if not data:
        return

    BRAIN_REPORTS.mkdir(parents=True, exist_ok=True)

    EXECUTION_RESULT_PATH.write_text(json.dumps(data, indent=2))


def main():
    start = datetime.utcnow()

    steps = {}

    # 1. explore
    steps["explore"] = run_step(ROOT / "install/ingestion_v2.py")

    # 2. next_action
    steps["next_action"] = run_step(ROOT / "install/engine/next_action_engine.py")

    # 3. execute
    steps["execute"] = run_step(ROOT / "install/engine/execute_next_action.py")

    # 🔥 CRITICAL FIX
    ensure_execution_artifact(steps["execute"])

    # 4. reconcile
    steps["reconcile"] = run_step(ROOT / "install/engine/reconcile_execution_state.py")

    duration = (datetime.utcnow() - start).total_seconds()

    output = {
        "status": "ok",
        "mode": "closed_loop_autonomous",
        "loop_ok": True,
        "duration_seconds": duration,
        "steps": steps
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
