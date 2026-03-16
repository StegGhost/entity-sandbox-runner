
from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/global_experiment_index.json")

@pipeline_contract(
    name="global_experiment_index",
    order=1780,
    tier=3,
    inputs=[],
    outputs=["observatory/global_experiment_index.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    result = {
        "module": "global_experiment_index",
        "status": "ok"
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
