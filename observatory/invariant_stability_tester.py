import json
from pathlib import Path

try:
    from observatory.pipeline_contract import pipeline_contract
except Exception:
    def pipeline_contract(**kwargs):
        def decorator(func):
            return func
        return decorator

@pipeline_contract(
    name="invariant_stability_tester",
    tier=3,
    order=930,
    inputs=["observatory/invariant_candidates.json"],
    outputs=["observatory/invariant_stability_results.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    input_path = Path("observatory/invariant_candidates.json")
    output_path = Path("observatory/invariant_stability_results.json")

    if input_path.exists():
        try:
            data = json.loads(input_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    else:
        data = {}

    if isinstance(data, dict):
        results = {}
        for name, value in data.items():
            if isinstance(value, dict):
                spread = (value.get("max", 0) or 0) - (value.get("min", 0) or 0)
                results[name] = {"spread": spread, "stable": spread < 1}
    else:
        results = {}

    payload = {"tested_invariants": len(results), "results": results}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"tested_invariants": len(results)}, indent=2))


if __name__ == "__main__":
    main()
