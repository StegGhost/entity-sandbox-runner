
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/distributed_campaign_coordinator.json")

def main():
    payload = {
        "service_module": "distributed_campaign_coordinator",
        "status": "ready",
        "note": "Coordinates distributed experiment campaigns."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
