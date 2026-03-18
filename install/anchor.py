import json

def anchor_hash(state):
    anchor = {
        "latest_hash": state.get("last_receipt"),
        "cycles": state.get("cycles")
    }
    json.dump(anchor, open("logs/anchor.json", "w"), indent=2)
