import json
from pathlib import Path
from observatory.pipeline_contract import pipeline_contract

INPUT = Path("observatory/equation_candidates.json")
OUTPUT = Path("observatory/discovery_novelty_engine.json")


@pipeline_contract(
    name="discovery_novelty_engine",
    order=474,
    tier=4,
    inputs=["observatory/equation_candidates.json"],
    outputs=["observatory/discovery_novelty_engine.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    keys = []
    if INPUT.exists():
        try:
            keys = list(json.loads(INPUT.read_text(encoding="utf-8")).keys())
        except Exception:
            keys = []
    payload = {
        "candidate_count": len(keys),
        "novelty_ranked": [{"candidate": k, "novelty": 1.0 / (i + 1)} for i, k in enumerate(keys[:50])],
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"candidate_count": len(keys)}, indent=2))


if __name__ == "__main__":
    main()
