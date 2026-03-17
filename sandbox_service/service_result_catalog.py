from pathlib import Path
import json

OUTPUT = Path("sandbox_service/service_result_catalog.json")

def main():
    payload = {
        "service_module": "service_result_catalog",
        "status": "ready",
        "note": "Indexes published service results and bundles."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
