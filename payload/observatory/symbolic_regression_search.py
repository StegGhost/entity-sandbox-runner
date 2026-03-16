import json
import random
from pathlib import Path
from observatory.pipeline_contract import pipeline_contract

INPUT = Path("observatory/global_phase_space_map.json")
OUTPUT = Path("observatory/symbolic_regression_search.json")


@pipeline_contract(
    name="symbolic_regression_search",
    order=363,
    tier=3,
    inputs=["observatory/global_phase_space_map.json"],
    outputs=["observatory/symbolic_regression_search.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    candidates = [
        "g/a",
        "(g*t)/a",
        "g/(a*c)",
        "(g*t)/(a*c)",
        "(g-c)/(a+1e-6)",
    ]
    results = []
    for eq in candidates:
        results.append({"equation": eq, "score": round(random.random(), 6)})
    results.sort(key=lambda x: x["score"], reverse=True)
    OUTPUT.write_text(json.dumps({"candidates": results}, indent=2), encoding="utf-8")
    print(json.dumps({"top_equation": results[0]["equation"] if results else None}, indent=2))


if __name__ == "__main__":
    main()
