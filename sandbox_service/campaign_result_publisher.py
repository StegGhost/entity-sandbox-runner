from pathlib import Path
import json

OUTPUT = Path("sandbox_service/campaign_result_publisher.json")

def main():
    payload = {
        "service_module": "campaign_result_publisher",
        "status": "ready",
        "note": "Publishes campaign-level outputs for review."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
