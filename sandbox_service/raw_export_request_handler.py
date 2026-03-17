import json
from pathlib import Path

OUT = Path("sandbox_service/raw_export_request_handler.json")

def main():
    payload = {
        "input": "sandbox_service/raw_export_request_registry.json",
        "output": "experiments/critical_ratio_campaign/raw_exports/",
        "status": "ready"
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
