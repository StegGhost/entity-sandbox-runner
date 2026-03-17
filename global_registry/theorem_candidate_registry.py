
from pathlib import Path
import json

OUTPUT = Path("global_registry/theorem_candidate_registry.json")

def main():
    payload = {
        "module": "theorem_candidate_registry",
        "status": "initialized",
        "note": "Registers theorem candidates derived from experiments."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
