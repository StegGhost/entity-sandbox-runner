import json
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
OUT = ROOT / "observatory" / "state_log" / "runtime_events.jsonl"

def record_runtime_event(event_type: str, payload: dict):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "payload": payload
    }
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

if __name__ == "__main__":
    print(json.dumps(record_runtime_event("manual_test", {"ok": True}), indent=2))
