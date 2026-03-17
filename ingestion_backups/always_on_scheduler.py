from pathlib import Path
import json

OUTPUT = Path("sandbox_service/always_on_scheduler.json")

def main():
    payload = {
        "module": "always_on_scheduler",
        "status": "initialized",
        "note": "Roadmap scaffold for upgrade 882."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
