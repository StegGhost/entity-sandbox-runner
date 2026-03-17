import json
from pathlib import Path

OUT = Path("observatory/parallel_shard_metadata.json")

def main():
    payload = {
        "fields": ["shard_id", "seed", "runs_per_shard", "artifact_path"],
        "status": "ready"
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
