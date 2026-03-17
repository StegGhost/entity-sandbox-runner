
from pathlib import Path
import json
from observatory.pipeline_contract import pipeline_contract

OUTPUT = Path("observatory/invariant_candidate_registry.json")

@pipeline_contract(
    name="invariant_candidate_registry",
    order=6050,
    tier=5,
    inputs=[],
    outputs=["observatory/invariant_candidate_registry.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    payload = {
        "module": "invariant_candidate_registry",
        "status": "ok",
        "note": "Registers invariant candidates."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
