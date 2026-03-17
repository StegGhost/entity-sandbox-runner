from pathlib import Path
import json

OUTPUT = Path("sandbox_service/artifact_manifest_exporter.json")

def main():
    payload = {
        "module": "artifact_manifest_exporter",
        "status": "initialized",
        "note": "Exports artifact manifests for user download."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
