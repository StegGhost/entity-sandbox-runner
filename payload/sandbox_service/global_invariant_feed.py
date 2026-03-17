from pathlib import Path
import json

OUTPUT = Path("sandbox_service/global_invariant_feed.json")

def main():
    payload = {
        "module": "global_invariant_feed",
        "status": "initialized",
        "note": "Roadmap scaffold for upgrade 890."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
