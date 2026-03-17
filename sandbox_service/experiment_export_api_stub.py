from pathlib import Path
import json

OUTPUT = Path("sandbox_service/experiment_export_api_stub.json")

def main():
    payload = {
        "module": "experiment_export_api_stub",
        "status": "initialized",
        "note": "Stub API for experiment export requests."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
