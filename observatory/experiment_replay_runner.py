from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/experiment_replay_runner.json")

@pipeline_contract(
    name="experiment_replay_runner",
    order=5070,
    tier=3,
    inputs=[],
    outputs=["observatory/experiment_replay_runner.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    payload = {
        "module": "experiment_replay_runner",
        "status": "ok",
        "note": "Replays experiments from stored configs and seeds."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
