from pathlib import Path
import json

OUTPUT = Path("publication_plane/demo_latest_pointer_builder.json")

def main():
    payload = {
        "module": "demo_latest_pointer_builder",
        "status": "initialized",
        "note": "Builds latest pointers for demo surfaces."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
