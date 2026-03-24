import json
import hashlib
from datetime import datetime

HISTORY_FILE = "history_stream.jsonl"

def _now():
    return datetime.utcnow().isoformat()

def _hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def append_event(event_type, payload):
    entry = {
        "ts": _now(),
        "event": event_type,
        "payload": payload
    }
    entry["state_hash"] = _hash(entry)

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    return entry

def record_bundle_result(bundle_name, status, violations=None):
    return append_event(
        "bundle_result",
        {
            "bundle": bundle_name,
            "status": status,
            "violations": violations or []
        }
    )

def read_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        return []

def main():
    record_bundle_result("test_bundle", "ok", [])
    print("history updated")

if __name__ == "__main__":
    main()
