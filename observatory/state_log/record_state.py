import json
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
STATE_DIR = ROOT / "observatory" / "state_log"
STATE_DIR.mkdir(parents=True, exist_ok=True)

def record_state(state):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "state": state
    }

    log_file = STATE_DIR / "system_states.jsonl"

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
