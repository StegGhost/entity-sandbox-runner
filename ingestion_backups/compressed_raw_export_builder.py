from pathlib import Path
import json

OUTPUT = Path("sandbox_service/compressed_raw_export_builder.json")

def main():
    payload = {
        "module": "compressed_raw_export_builder",
        "status": "initialized",
        "note": "Creates compressed raw exports from shard outputs."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
