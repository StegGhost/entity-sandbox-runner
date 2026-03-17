
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/adaptive_run_allocator.json")

def main():
    payload = {
        "service_module": "adaptive_run_allocator",
        "status": "ready",
        "note": "Allocates compute to highest-value runs."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
