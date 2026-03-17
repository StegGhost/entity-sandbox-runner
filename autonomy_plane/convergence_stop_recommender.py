from pathlib import Path
import json

OUTPUT = Path("autonomy_plane/convergence_stop_recommender.json")

def main():
    payload = {
        "module": "convergence_stop_recommender",
        "status": "initialized",
        "note": "Recommends stopping when Uc stabilizes."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
