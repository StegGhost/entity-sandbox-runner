from pathlib import Path
import json
import time

def replay(path: str = "observatory/experiment_timeline.json", delay: float = 0.05):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    events = json.loads(p.read_text(encoding="utf-8"))
    for e in events:
        print(e)
        time.sleep(delay)
