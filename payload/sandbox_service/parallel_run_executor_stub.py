from pathlib import Path
import json

OUTPUT = Path("sandbox_service/parallel_run_executor_stub.json")

def main():
    payload = {
        "service_module": "parallel_run_executor_stub",
        "status": "ready",
        "note": "Executes parallel-run experiment requests through the service layer."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
