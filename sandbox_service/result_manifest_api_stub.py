from pathlib import Path
import json

OUTPUT = Path("sandbox_service/result_manifest_api_stub.json")

def main():
    payload = {
        "service_module": "result_manifest_api_stub",
        "status": "ready",
        "note": "Publishes service-facing result manifest data."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
