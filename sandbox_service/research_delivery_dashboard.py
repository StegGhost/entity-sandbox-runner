from pathlib import Path
import json

OUTPUT = Path("sandbox_service/research_delivery_dashboard.json")

def main():
    payload = {
        "service_module": "research_delivery_dashboard",
        "status": "ready",
        "note": "Builds delivery-facing dashboard data."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
