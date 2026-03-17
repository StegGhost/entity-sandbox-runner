from pathlib import Path
import json

OUTPUT = Path("sandbox_service/merge_job_trigger_stub.json")

def main():
    payload = {
        "service_module": "merge_job_trigger_stub",
        "status": "ready",
        "note": "Prepares and triggers merge jobs after shard completion."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
