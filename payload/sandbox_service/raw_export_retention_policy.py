from pathlib import Path
import json

OUTPUT = Path("sandbox_service/raw_export_retention_policy.json")

def main():
    payload = {
        "service_module": "raw_export_retention_policy",
        "status": "ready",
        "note": "Tracks retention windows for raw export archives."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
