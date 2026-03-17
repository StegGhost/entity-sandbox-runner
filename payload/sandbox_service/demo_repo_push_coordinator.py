from pathlib import Path
import json

OUTPUT = Path("sandbox_service/demo_repo_push_coordinator.json")

def main():
    payload = {
        "service_module": "demo_repo_push_coordinator",
        "status": "ready",
        "note": "Coordinates push-ready updates for the demo repo."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
