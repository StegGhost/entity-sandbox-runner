import json
from pathlib import Path

OUT = Path("observatory/campaign_merge_validator.json")

def main():
    payload = {
        "checks": ["shard_count", "merged_sample_count", "duplicate_detection"],
        "status": "ready"
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
