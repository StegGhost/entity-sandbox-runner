import json
from pathlib import Path
from observatory.pipeline_contract import pipeline_contract

INPUT = Path("observatory/control_law_synthesizer.json")
OUTPUT = Path("observatory/adaptive_intervention_planner.json")


@pipeline_contract(
    name="adaptive_intervention_planner",
    order=365,
    tier=3,
    inputs=["observatory/control_law_synthesizer.json"],
    outputs=["observatory/adaptive_intervention_planner.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    laws = []
    if INPUT.exists():
        laws = json.loads(INPUT.read_text(encoding="utf-8")).get("laws", [])
    plans = []
    for i, law in enumerate(laws[:25]):
        plans.append({
            "plan_id": f"PLAN_{i:04}",
            "trigger": law.get("condition"),
            "intervention": law.get("action"),
            "priority": "high",
        })
    payload = {"plan_count": len(plans), "plans": plans}
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"plan_count": len(plans)}, indent=2))


if __name__ == "__main__":
    main()
