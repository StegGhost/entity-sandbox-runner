from pathlib import Path
import json

OUTPUT = Path("sandbox_service/experiment_cost_estimator.json")

def main():
    result = {
        "service_module": "experiment_cost_estimator",
        "status": "ready",
        "note": "Estimates cost envelopes for experiments."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
