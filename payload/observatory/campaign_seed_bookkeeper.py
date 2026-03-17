import json
from pathlib import Path

OUT = Path("observatory/campaign_seed_bookkeeper.json")

def main():
    payload = {
        "seed_strategy": "deterministic_per_shard",
        "seed_namespace": "critical_ratio_campaign",
        "status": "ready"
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
