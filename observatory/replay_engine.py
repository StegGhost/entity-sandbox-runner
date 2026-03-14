import json
import time

def replay(path="observatory/experiment_timeline.json", delay=0.05):

    events = json.load(open(path))

    for e in events:

        print(
            f"step {e['step']} "
            f"pressure={e['artifact_pressure']} "
            f"bound={e['bound']} "
            f"admissible={e['admissible']}"
        )

        time.sleep(delay)


if __name__ == "__main__":
    replay()
