from pathlib import Path
from datetime import datetime, timezone
import json

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def write_receipts(exp_name: str, receipts: list[dict]):
    runs = Path("receipts/runs")
    chains = Path("receipts/chains")
    runs.mkdir(parents=True, exist_ok=True)
    chains.mkdir(parents=True, exist_ok=True)

    run_path = runs / f"{exp_name}_receipts.jsonl"
    chain_path = chains / f"{exp_name}_chain.json"

    with open(run_path, "w", encoding="utf-8") as f:
        prev = None
        ids = []
        for idx, r in enumerate(receipts, start=1):
            receipt_id = f"{exp_name}_rcpt_{idx:04d}"
            payload = {
                "receipt_id": receipt_id,
                "chain_prev": prev,
                "timestamp_utc": _now(),
                **r,
            }
            ids.append(receipt_id)
            prev = receipt_id
            f.write(json.dumps(payload) + "\n")

    chain = {
        "experiment_id": exp_name,
        "generated_at_utc": _now(),
        "receipt_ids": ids,
        "run_receipts_file": str(run_path),
    }
    chain_path.write_text(json.dumps(chain, indent=2), encoding="utf-8")
    return str(run_path), str(chain_path)
