import json
from pathlib import Path

try:
    from observatory.pipeline_contract import pipeline_contract
except Exception:
    def pipeline_contract(**kwargs):
        def decorator(func):
            return func
        return decorator

import subprocess
import sys

@pipeline_contract(
    name="autonomous_research_supervisor",
    tier=5,
    order=1000,
    inputs=[],
    outputs=["observatory/research_supervisor_report.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    pipeline = [
        "observatory/symbolic_regression_engine.py",
        "observatory/discovery_graph_engine.py",
        "observatory/invariant_stability_tester.py",
        "observatory/anomaly_discovery_engine.py",
    ]

    results = []
    for step in pipeline:
        path = Path(step)
        if not path.exists():
            results.append({"step": step, "status": "missing"})
            continue
        subprocess.run([sys.executable, str(path)], check=False)
        results.append({"step": step, "status": "attempted"})

    output_path = Path("observatory/research_supervisor_report.json")
    payload = {"steps": results, "status": "complete"}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"steps": len(results), "status": "complete"}, indent=2))


if __name__ == "__main__":
    main()
