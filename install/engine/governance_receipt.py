
import json, hashlib, datetime
from pathlib import Path

OUT = Path("logs/governance_receipts.json")

def record_receipt(manifest, decision, stage):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "time": datetime.datetime.utcnow().isoformat(),
        "bundle": manifest.get("bundle_name"),
        "stage": stage,
        "decision": decision,
        "hash": hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    }
    data = []
    if OUT.exists():
        data = json.loads(OUT.read_text())
    data.append(entry)
    OUT.write_text(json.dumps(data, indent=2))
