from pathlib import Path
import json

OUTPUT = Path("sandbox_service/artifact_download_index.json")

def main():
    payload = {
        "service_module": "artifact_download_index",
        "status": "ready",
        "note": "Indexes downloadable artifacts and export bundles."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
