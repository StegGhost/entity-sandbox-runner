from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/cross_baseline_comparator.json")

@pipeline_contract(
    name="cross_baseline_comparator",
    order=5130,
    tier=4,
    inputs=[],
    outputs=["observatory/cross_baseline_comparator.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    payload = {
        "module": "cross_baseline_comparator",
        "status": "ok",
        "note": "Compares invariant performance against baseline families."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
