import json
import hashlib
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
LEDGER = ROOT / "observatory" / "state_log" / "runtime_ledger.jsonl"

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _last_entry_hash():
    if not LEDGER.exists():
        return None
    last = None
    with open(LEDGER, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                last = json.loads(line)
    return None if last is None else last.get("entry_hash")

def append_ledger(event_type: str, payload: dict):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "payload": payload,
        "previous_hash": _last_entry_hash(),
    }
    entry["entry_hash"] = sha256_text(json.dumps(entry, sort_keys=True))
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

if __name__ == "__main__":
    print(json.dumps(append_ledger("manual_test", {"ok": True}), indent=2))
