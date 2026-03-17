
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/research_node_registration_api.json")

def main():
    payload = {
        "module": "research_node_registration_api",
        "status": "initialized",
        "note": "Registers research nodes."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
