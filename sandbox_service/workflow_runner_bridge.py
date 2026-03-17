from pathlib import Path
import json

OUTPUT = Path("sandbox_service/workflow_runner_bridge.json")

def main():
    payload = {
        "service_module": "workflow_runner_bridge",
        "status": "ready",
        "note": "Bridges workflow-dispatch inputs to execution plans."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
