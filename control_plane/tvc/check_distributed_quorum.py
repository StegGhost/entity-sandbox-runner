import json
import urllib.request
import sys
from pathlib import Path

CONFIG = Path(__file__).parent / "distributed_quorum.json"


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return json.loads(r.read())
    except:
        return None


def fail(reason):
    print(json.dumps({"status": "invalid", "reason": reason}, indent=2))
    sys.exit(1)


def main():
    config = json.loads(CONFIG.read_text())

    approvals = 0

    for node in config["nodes"]:
        res = fetch(node["url"])
        if res and res.get("approved") is True:
            approvals += 1

    if approvals < config["required"]:
        fail("distributed_quorum_not_met")

    print(json.dumps({
        "status": "ok",
        "approvals": approvals
    }, indent=2))


if __name__ == "__main__":
    main()
