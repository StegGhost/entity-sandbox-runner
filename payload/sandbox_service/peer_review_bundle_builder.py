
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/peer_review_bundle_builder.json")

def main():
    payload = {
        "service_module": "peer_review_bundle_builder",
        "status": "ready",
        "note": "Builds bundles for peer review."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
