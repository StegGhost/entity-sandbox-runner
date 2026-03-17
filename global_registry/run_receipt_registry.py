from pathlib import Path
import json

OUTPUT = Path("global_registry/run_receipt_registry.json")

def main():
    payload = {
        "module": "run_receipt_registry",
        "status": "initialized",
        "note": "Registers campaign run receipts globally."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
