from pathlib import Path
import json

OUTPUT = Path("sandbox_service/delivery_profile_resolver.json")

def main():
    payload = {
        "service_module": "delivery_profile_resolver",
        "status": "ready",
        "note": "Resolves summary/standard/raw delivery for each request."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
