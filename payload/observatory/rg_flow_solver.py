import json
from pathlib import Path
from observatory.pipeline_contract import pipeline_contract

INPUT = Path("observatory/global_phase_space_map.json")
OUTPUT = Path("observatory/rg_flow_solver.json")


def load_points():
    if not INPUT.exists():
        return []
    return json.loads(INPUT.read_text(encoding="utf-8")).get("phase_space", [])


@pipeline_contract(
    name="rg_flow_solver",
    order=361,
    tier=3,
    inputs=["observatory/global_phase_space_map.json"],
    outputs=["observatory/rg_flow_solver.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    points = load_points()
    flow = []
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        flow.append({
            "from_index": i,
            "to_index": i + 1,
            "delta_capacity": (p2.get("governance_capacity") or 0) - (p1.get("governance_capacity") or 0),
            "delta_pressure": (p2.get("artifact_pressure") or 0) - (p1.get("artifact_pressure") or 0),
            "delta_constraints": (p2.get("constraints") or p2.get("constraint_pressure") or 0) - (p1.get("constraints") or p1.get("constraint_pressure") or 0),
            "delta_trust": (p2.get("trust_continuity") or 0) - (p1.get("trust_continuity") or 0),
        })
    payload = {"step_count": len(flow), "flow": flow[:500]}
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"step_count": len(flow)}, indent=2))


if __name__ == "__main__":
    main()
