#!/usr/bin/env python3
"""Promote staged workflow into .github/workflows/ when approved."""

from pathlib import Path
import shutil

SRC = Path("payload/workflows/run_evaluation.yml")
DST = Path(".github/workflows/run_evaluation.yml")

def main():
    if not SRC.exists():
        raise SystemExit(f"Missing staged workflow: {SRC}")
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, DST)
    print(f"Promoted {SRC} -> {DST}")

if __name__ == "__main__":
    main()
