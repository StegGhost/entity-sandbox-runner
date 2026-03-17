from pathlib import Path
import json

OUTPUT = Path("sandbox_service/researcher_delivery_preferences.json")

def main():
    payload = {
        "service_module": "researcher_delivery_preferences",
        "status": "ready",
        "note": "Stores researcher preferences for summary, standard, or raw delivery."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
