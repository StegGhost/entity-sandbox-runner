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
    name="anomaly_discovery_engine",
    tier=4,
    order=980,
    inputs=["observatory/global_phase_space_map.json"],
    outputs=["observatory/anomalies.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    input_path = Path("observatory/global_phase_space_map.json")
    output_path = Path("observatory/anomalies.json")

    if input_path.exists():
        try:
            points = json.loads(input_path.read_text(encoding="utf-8")).get("phase_space", [])
        except Exception:
            points = []
    else:
        points = []

    anomalies = []
    for p in points:
        vm = p.get("viability_margin", 0) or 0
        if abs(vm) > 1:
            anomalies.append(p)

    payload = {"anomaly_count": len(anomalies), "anomalies": anomalies[:50]}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"anomaly_count": len(anomalies)}, indent=2))


if __name__ == "__main__":
    main()
