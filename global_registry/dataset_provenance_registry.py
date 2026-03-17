
from pathlib import Path
import json

OUTPUT = Path("global_registry/dataset_provenance_registry.json")

def main():
    payload = {
        "module": "dataset_provenance_registry",
        "status": "initialized",
        "note": "Records dataset provenance for reproducibility."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
