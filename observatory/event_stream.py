from pathlib import Path
from datetime import datetime, timezone
import json

STREAM_FILE = Path("observatory/event_stream.jsonl")
STREAM_FILE.parent.mkdir(parents=True, exist_ok=True)

def publish_event(event_type: str, payload: dict) -> None:
    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "payload": payload,
    }
    with open(STREAM_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
