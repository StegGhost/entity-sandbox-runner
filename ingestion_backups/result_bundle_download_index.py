from pathlib import Path
import json

OUTPUT = Path("sandbox_service/result_bundle_download_index.json")

def main():
    payload = {
        "module": "result_bundle_download_index",
        "status": "initialized",
        "note": "Indexes downloadable result bundles."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
