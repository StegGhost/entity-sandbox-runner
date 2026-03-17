from pathlib import Path
import json

OUTPUT = Path("sandbox_service/artifact_retention_manifest.json")

def main():
    payload = {
        "module": "artifact_retention_manifest",
        "status": "initialized",
        "note": "Tracks retention of bundles and logs."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
