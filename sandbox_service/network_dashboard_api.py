
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/network_dashboard_api.json")

def main():
    payload = {
        "module": "network_dashboard_api",
        "status": "initialized",
        "note": "Provides dashboard data."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
