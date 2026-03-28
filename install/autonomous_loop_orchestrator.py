import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "brain_reports"

NEXT_ACTION = REPORT_DIR / "next_action.json"
EXECUTION = REPORT_DIR / "execution_result.json"
RECONCILE = REPORT_DIR / "reconcile_result.json"
SUMMARY = REPORT_DIR / "loop_summary.json"


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def load(path):
    try:
        return json.loads(path.read_text())
    except:
        return None


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def main():
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")

    run(["python", "install/ingestion_v2.py"])
    run(["python", "install/engine/next_action_engine.py"])
    run(["python", "install/engine/execute_next_action.py"])
    run(["python", "install/engine/reconcile_execution_state.py"])

    reconcile = load(RECONCILE)

    status = "invalid"
    reason = "unknown"

    if reconcile:
        if reconcile.get("status") == "ok":
            status = "ok"
            reason = reconcile.get("reason")

    summary = {
        "status": status,
        "reason": reason,
        "ts": ts
    }

    write(SUMMARY, summary)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
