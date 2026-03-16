import json
from pathlib import Path
from observatory.pipeline_contract import pipeline_contract

INPUT = Path("observatory/global_phase_space_map.json")
OUTPUT = Path("observatory/stability_manifold_explorer.json")


@pipeline_contract(
    name="stability_manifold_explorer",
    order=471,
    tier=4,
    inputs=["observatory/global_phase_space_map.json"],
    outputs=["observatory/stability_manifold_explorer.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    if not INPUT.exists():
        payload = {"points": [], "summary": {"total": 0}}
    else:
        points = json.loads(INPUT.read_text(encoding="utf-8")).get("phase_space", [])
        payload = {
            "points": [
                {
                    "x": p.get("governance_capacity"),
                    "y": p.get("artifact_pressure"),
                    "z": p.get("viability_margin"),
                    "region": p.get("region"),
                }
                for p in points[:1000]
            ],
            "summary": {"total": len(points)},
        }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
