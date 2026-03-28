import json
import sys
from pathlib import Path

REPORT_DIR = Path("brain_reports")


def load(name):
    path = REPORT_DIR / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    gate = load("stegcore_gate_result.json")

    if not gate:
        print("❌ Missing StegCore gate result")
        sys.exit(1)

    if not gate.get("admissible"):
        print("❌ COMMIT BLOCKED: inadmissible state")
        print(json.dumps(gate, indent=2))
        sys.exit(1)

    print("✅ COMMIT APPROVED")


if __name__ == "__main__":
    main()
