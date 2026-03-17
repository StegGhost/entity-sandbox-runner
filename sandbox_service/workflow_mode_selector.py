import json
from pathlib import Path

OUT = Path("sandbox_service/workflow_mode_selector.json")

def main():
    schema = json.loads(Path("sandbox_service/run_mode_schema.json").read_text(encoding="utf-8"))
    payload = {
        "available_modes": schema["modes"],
        "default_mode": schema["default_mode"],
        "max_shards": schema["max_shards"]
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
