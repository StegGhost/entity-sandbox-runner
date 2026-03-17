from pathlib import Path
import json

OUTPUT = Path("sandbox_service/node_capability_query_api.json")

def main():
    payload = {
        "service_module": "node_capability_query_api",
        "status": "ready",
        "note": "Returns node and worker capabilities."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
