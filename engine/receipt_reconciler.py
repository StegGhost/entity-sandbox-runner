import os
import json
from datetime import datetime

ROOT = os.getcwd()

RECEIPT_DIR = os.path.join(ROOT, "receipts")
OUTPUT_DIR = os.path.join(ROOT, "brain_reports")

CATALOG_PATH = os.path.join(OUTPUT_DIR, "receipt_catalog.json")
INDEX_PATH = os.path.join(OUTPUT_DIR, "receipt_index.jsonl")
STATE_PATH = os.path.join(OUTPUT_DIR, "receipt_reconciled_state.json")


def discover_receipts():
    receipts = []

    for root, _, files in os.walk(RECEIPT_DIR):
        for f in files:
            if f.endswith(".json"):
                full_path = os.path.join(root, f)
                receipts.append(full_path)

    return receipts


def load_receipt(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {"_corrupt": True, "path": path}


def build_catalog(receipts):
    catalog = []

    for path in receipts:
        data = load_receipt(path)

        entry = {
            "path": path,
            "ts": data.get("ts"),
            "action": data.get("action"),
            "status": data.get("status"),
        }

        catalog.append(entry)

    return catalog


def write_outputs(catalog):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # catalog (full snapshot)
    with open(CATALOG_PATH, "w") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat(),
            "count": len(catalog),
            "receipts": catalog
        }, f, indent=2)

    # index (append-only)
    with open(INDEX_PATH, "a") as f:
        for r in catalog:
            f.write(json.dumps(r) + "\n")

    # reconciled state (latest view)
    state = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_receipts": len(catalog),
        "latest_receipts": catalog[-20:]
    }

    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def main():
    receipts = discover_receipts()
    catalog = build_catalog(receipts)
    write_outputs(catalog)

    print(json.dumps({
        "status": "ok",
        "receipts_found": len(receipts),
        "output_dir": OUTPUT_DIR
    }, indent=2))


if __name__ == "__main__":
    main()
