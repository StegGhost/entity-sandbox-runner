import json
import time
from pathlib import Path

STREAM = Path("observatory/live_stream.jsonl")

def watch():

    seen = 0

    print("Watching live stream...")

    while True:

        if STREAM.exists():

            lines = STREAM.read_text().splitlines()

            for line in lines[seen:]:

                event = json.loads(line)

                print(
                    f"step {event['step']} | "
                    f"A={event['artifact_pressure']:.3f} "
                    f"G={event['governance_capacity']:.3f} "
                    f"bound={event['bound']:.3f} "
                    f"admissible={event['admissible']}"
                )

            seen = len(lines)

        time.sleep(0.2)


if __name__ == "__main__":
    watch()
