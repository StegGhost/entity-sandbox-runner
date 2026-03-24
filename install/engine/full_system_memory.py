import json
from pathlib import Path

def build_memory_snapshot(history_path="history_stream.jsonl"):
    events = []
    p = Path(history_path)
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
    return {
        "event_count": len(events),
        "last_event_type": events[-1]["event_type"] if events else None,
        "events": events
    }

def main(output_path="full_system_memory.json"):
    snapshot = build_memory_snapshot()
    Path(output_path).write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()
