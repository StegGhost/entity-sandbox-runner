
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/experiment_marketplace.json")

def main():
    result = {
        "service_module": "experiment_marketplace",
        "status": "ready"
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(result)

if __name__ == "__main__":
    main()
