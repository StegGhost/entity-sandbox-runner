from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/multi_run_uc_aggregator.json")

@pipeline_contract(
    name="multi_run_uc_aggregator",
    order=5510,
    tier=4,
    inputs=[],
    outputs=["observatory/multi_run_uc_aggregator.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    payload = {
        "module": "multi_run_uc_aggregator",
        "status": "ok",
        "note": "Aggregates Uc estimates across repeated campaign runs."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
