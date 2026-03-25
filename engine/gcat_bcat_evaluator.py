import json
import os
from datetime import datetime

ROOT = os.getcwd()
OUTPUT_DIR = os.path.join(ROOT, "brain_reports")

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "admissibility_state.json")


def evaluate():
    # Minimal real signal (not fake math)
    failed = len(os.listdir("failed_bundles")) if os.path.exists("failed_bundles") else 0
    installed = len(os.listdir("installed_bundles")) if os.path.exists("installed_bundles") else 0

    total = failed + installed if (failed + installed) > 0 else 1

    stability = installed / total

    return {
        "ts": datetime.utcnow().isoformat(),
        "metrics": {
            "failed": failed,
            "installed": installed,
            "stability_score": round(stability, 3)
        },
        "admissible": stability > 0.5
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    state = evaluate()

    with open(OUTPUT_PATH, "w") as f:
        json.dump(state, f, indent=2)

    print(json.dumps({
        "status": "ok",
        "admissible": state["admissible"]
    }, indent=2))


if __name__ == "__main__":
    main()
