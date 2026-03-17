from pathlib import Path
import json

OUTPUT = Path("sandbox_service/peer_dataset_request_handler.json")

def main():
    payload = {
        "service_module": "peer_dataset_request_handler",
        "status": "ready",
        "note": "Handles peer dataset requests."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
