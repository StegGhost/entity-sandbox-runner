
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/researcher_invariant_query_api.json")

def main():
    payload = {
        "service_module": "researcher_invariant_query_api",
        "status": "ready",
        "note": "Provides invariant query API."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
