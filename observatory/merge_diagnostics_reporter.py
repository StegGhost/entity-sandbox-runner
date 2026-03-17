from pathlib import Path
import json

OUTPUT = Path("observatory/merge_diagnostics_reporter.json")

def main():
    payload = {
        "module": "merge_diagnostics_reporter",
        "status": "initialized",
        "note": "Writes detailed diagnostics for merge outcomes."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
