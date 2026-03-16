from pathlib import Path
import json

OUTPUT = Path("sandbox_service/remote_job_queue.json")

def main():
    result = {
        "service_module": "remote_job_queue",
        "status": "ready",
        "note": "Queues remote experiment submissions."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
