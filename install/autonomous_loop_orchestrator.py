import subprocess
import json
import time
import os

STEPS = [
    ("document_compactor", ["python", "install/document_compactor.py"]),
    ("canonical_feedback", ["python", "install/canonical_feedback.py"]),
    ("knowledge_delta", ["python", "install/knowledge_delta.py"]),
    ("canonical_receipt_binder", ["python", "install/canonical_receipt_binder.py"]),
    ("feedback_injection", ["python", "install/feedback_injection.py"]),
    ("feedback_execution_bridge", ["python", "install/feedback_execution_bridge.py"]),
]

OUTPUT_REPORT = "payload/runtime/autonomous_loop_report.json"

def run_step(name, cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "step": name,
        "cmd": cmd,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }

def main():
    os.makedirs("payload/runtime", exist_ok=True)

    report = {
        "timestamp": time.time(),
        "steps": []
    }

    for name, cmd in STEPS:
        step_result = run_step(name, cmd)
        report["steps"].append(step_result)

        if step_result["returncode"] != 0:
            report["status"] = "failed"
            break
    else:
        report["status"] = "ok"

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps({
        "status": report["status"],
        "report": OUTPUT_REPORT
    }, indent=2))

    if report["status"] != "ok":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
