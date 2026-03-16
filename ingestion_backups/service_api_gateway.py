from pathlib import Path
import json

OUTPUT = Path("sandbox_service/service_api_gateway.json")

def main():
    result = {
        "service_module": "service_api_gateway",
        "status": "ready",
        "note": "Routes Sandbox-as-a-Service API requests."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
