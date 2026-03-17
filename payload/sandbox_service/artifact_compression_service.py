
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/artifact_compression_service.json")

def main():
    payload = {
        "module": "artifact_compression_service",
        "status": "initialized",
        "note": "Compresses large experiment outputs."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
