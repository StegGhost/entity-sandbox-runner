from pathlib import Path
import json

OUTPUT = Path("autonomy_plane/exploration_reward_model.json")

def main():
    payload = {
        "module": "exploration_reward_model",
        "status": "initialized",
        "note": "Roadmap scaffold for upgrade 788."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
