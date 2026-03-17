
from pathlib import Path
import json

OUTPUT = Path("replication_plane/experiment_replication_dispatcher.json")

def main():
    payload = {
        "module": "experiment_replication_dispatcher",
        "status": "initialized",
        "note": "Dispatches replication campaigns."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
