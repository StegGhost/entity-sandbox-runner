import json
import hashlib
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
RECEIPT_DIR = ROOT / "evidence_plane" / "receipts"
RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def record_install(bundle_name, files):
    receipt = {
        "bundle": bundle_name,
        "timestamp": datetime.utcnow().isoformat(),
        "files": {}
    }

    for f in files:
        p = Path(f)
        if p.exists():
            receipt["files"][str(p)] = hash_file(p)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out = RECEIPT_DIR / f"{bundle_name}_{ts}.json"

    with open(out, "w") as f:
        json.dump(receipt, f, indent=2)

    return out
