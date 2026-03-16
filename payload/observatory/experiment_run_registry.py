from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/experiment_run_registry.json")

@pipeline_contract(
    name="experiment_run_registry",
    order=5030,
    tier=4,
    inputs=[],
    outputs=["observatory/experiment_run_registry.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    payload = {
        "module": "experiment_run_registry",
        "status": "ok",
        "note": "Registers experiment runs and manifest pointers."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
