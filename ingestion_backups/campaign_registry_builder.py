from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/campaign_registry_builder.json")

@pipeline_contract(
    name="campaign_registry_builder",
    order=4910,
    tier=4,
    inputs=[],
    outputs=["observatory/campaign_registry_builder.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    result = {
        "module": "campaign_registry_builder",
        "status": "ok",
        "note": "Registers experiment campaigns and their artifacts."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
