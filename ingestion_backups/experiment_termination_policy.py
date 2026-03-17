from pathlib import Path
import json

OUTPUT = Path("discovery_engine/experiment_termination_policy.json")

def main():
    payload = {
        "module": "experiment_termination_policy",
        "status": "initialized",
        "note": "Roadmap scaffold for upgrade 813."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
