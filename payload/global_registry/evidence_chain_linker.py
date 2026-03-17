
from pathlib import Path
import json

OUTPUT = Path("global_registry/evidence_chain_linker.json")

def main():
    payload = {
        "module": "evidence_chain_linker",
        "status": "initialized",
        "note": "Links experiment receipts to invariant claims."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
