import subprocess
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "brain_reports"


def run_step(name, cmd):
    print(f"\n=== RUNNING: {name} ===")

    start = time.time()

    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True
    )

    duration = round(time.time() - start, 3)

    result = {
        "name": name,
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "duration": duration
    }

    print(json.dumps(result, indent=2))

    return result


def write_trace(trace):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "orchestrator_trace.json"
    path.write_text(json.dumps(trace, indent=2), encoding="utf-8")


def main():
    trace = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "steps": []
    }

    steps = [
        ("ingestion", ["python", "install/ingestion_v2.py"]),
        ("next_action", ["python", "install/engine/next_action_engine.py"]),
        ("execute", ["python", "install/engine/execute_next_action.py"]),
        ("reconcile", ["python", "install/engine/reconcile_execution_state.py"]),
    ]

    for name, cmd in steps:
        result = run_step(name, cmd)
        trace["steps"].append(result)

    write_trace(trace)

    print("\n=== ORCHESTRATOR COMPLETE ===")


if __name__ == "__main__":
    main()
