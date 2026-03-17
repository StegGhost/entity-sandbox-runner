import json
from pathlib import Path

OUT = Path("sandbox_service/parallel_result_merger.json")

def main():
    payload = {
        "input_pattern": "experiments/critical_ratio_campaign/results/shards/*.json",
        "output": "experiments/critical_ratio_campaign/results/phase_space_map.json",
        "status": "ready"
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
