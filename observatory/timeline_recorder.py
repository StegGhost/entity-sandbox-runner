import json
from pathlib import Path

def build_timeline(stream_file="observatory/live_stream.jsonl"):

    p = Path(stream_file)
    events = []

    if not p.exists():
        print("No stream file found.")
        return None

    with open(p) as f:
        for line in f:
            events.append(json.loads(line))

    out = Path("observatory/experiment_timeline.json")
    out.write_text(json.dumps(events, indent=2))

    print("Timeline written:", out)
    return str(out)


if __name__ == "__main__":
    build_timeline()
