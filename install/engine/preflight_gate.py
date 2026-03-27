import json
import os
import time

ROOT = os.getcwd()
REPORT_DIR = os.path.join(ROOT, "brain_reports")
os.makedirs(REPORT_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(REPORT_DIR, "preflight_decision.json")

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def main():
    result = {
        "status": "ok",
        "ts": now(),
        "decision": {
            "decision": "run_experiment",
            "reason": "default_allow"
        }
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps({
        "status": "ok",
        "output": OUTPUT_PATH,
        "result": result
    }, indent=2))


if __name__ == "__main__":
    main()
