from pathlib import Path
import json

OUTPUT = Path("sandbox_service/peer_bundle_exchange.json")

def main():
    payload = {
        "service_module": "peer_bundle_exchange",
        "status": "ready",
        "note": "Exchanges campaign bundles across peers."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
