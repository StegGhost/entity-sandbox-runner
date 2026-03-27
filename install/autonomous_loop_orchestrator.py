import json
import os
import subprocess
from datetime import datetime

ROOT = os.getcwd()

REPORT_PATH = "payload/runtime/autonomous_loop_report.json"


def run_step(name, cmd):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "output_snippet": result.stdout[-2000:]
        }
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }


def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def main():
    start = datetime.utcnow()

    steps = {}

    # --- EXPLORE ---
    steps["explore"] = run_step(
        "explore",
        ["python", "-m", "install.explorer"]
    )

    # --- NEXT ACTION ---
    steps["next_action"] = run_step(
        "next_action",
        ["python", "-m", "install.engine.next_action_engine"]
    )

    next_action_data = load_json("brain_reports/next_action.json")

    # --- EXECUTE ---
    steps["execute"] = run_step(
        "execute",
        ["python", "-m", "install.engine.execute_next_action"]
    )

    # --- RECONCILE ---
    steps["reconcile"] = run_step(
        "reconcile",
        ["python", "-m", "install.engine.reconcile_execution_state"]
    )

    duration = (datetime.utcnow() - start).total_seconds()

    report = {
        "status": "ok",
        "mode": "sandbox_loop_with_observer",
        "loop_ok": True,
        "duration_seconds": duration,
        "timestamp": start.timestamp(),
        "steps": steps,
        "next_action": next_action_data,
        "artifacts": {
            "explore": "brain_reports/explore.json",
            "next_action": "brain_reports/next_action.json",
            "execution_result": "brain_reports/execute_next_action_result.json",
            "reconciled_state": "brain_reports/reconciled_state.json"
        }
    }

    os.makedirs("payload/runtime", exist_ok=True)

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
