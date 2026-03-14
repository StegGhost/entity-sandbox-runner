import argparse
from pathlib import Path
import json
from sandbox.phase_space import build_phase_space_visuals

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    args = parser.parse_args()
    summary = build_phase_space_visuals(Path(args.results))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
