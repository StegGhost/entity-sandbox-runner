
from pathlib import Path
import json

OUTPUT = Path("observatory/global_phase_space_aggregator.json")

def main():
    payload = {
        "module": "global_phase_space_aggregator",
        "status": "initialized",
        "note": "Aggregates phase-space maps globally."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
