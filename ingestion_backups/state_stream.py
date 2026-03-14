import json
from pathlib import Path
from datetime import datetime

STREAM_FILE = Path("observatory/live_stream.jsonl")
STREAM_FILE.parent.mkdir(parents=True, exist_ok=True)

def emit_state(event):

    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        **event
    }

    with open(STREAM_FILE, "a") as f:
        f.write(json.dumps(payload) + "\n")
