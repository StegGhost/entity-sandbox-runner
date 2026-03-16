from pathlib import Path
import json

OUTPUT = Path("sandbox_service/artifact_merge_coordinator.json")

def main():
    payload = {
        "service_module": "artifact_merge_coordinator",
        "status": "ready",
        "note": "Coordinates shard artifact merging."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
