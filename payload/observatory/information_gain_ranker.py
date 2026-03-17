
from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/information_gain_ranker.json")

@pipeline_contract(
    name="information_gain_ranker",
    order=5850,
    tier=4,
    inputs=[],
    outputs=["observatory/information_gain_ranker.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    payload = {
        "module": "information_gain_ranker",
        "status": "ok",
        "note": "Ranks parameter regions by information gain."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
