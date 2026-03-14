from __future__ import annotations

import argparse
import json
from pathlib import Path

from sandbox.phase_space import build_phase_space_visuals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, help="path to results json")
    args = parser.parse_args()

    results_path = Path(args.results).resolve()
    summary = build_phase_space_visuals(results_path)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()