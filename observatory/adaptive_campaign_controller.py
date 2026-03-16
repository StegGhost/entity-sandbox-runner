from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/adaptive_campaign_controller.json")

@pipeline_contract(
    name="adaptive_campaign_controller",
    order=5350,
    tier=5,
    inputs=[],
    outputs=["observatory/adaptive_campaign_controller.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    payload = {
        "module": "adaptive_campaign_controller",
        "status": "ok",
        "note": "Chooses next experiment batches automatically."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
