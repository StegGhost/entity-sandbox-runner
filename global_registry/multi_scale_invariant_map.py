
from pathlib import Path
import json

OUTPUT = Path("global_registry/multi_scale_invariant_map.json")

def main():
    payload = {
        "module": "multi_scale_invariant_map",
        "status": "initialized",
        "note": "Maps invariants across scales."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
