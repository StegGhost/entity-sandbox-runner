#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def promote_workflows():
    src_dir = Path("payload/workflows")
    dst_dir = Path(".github/workflows")

    if not src_dir.exists():
        print("No workflow payload directory found")
        return 0

    dst_dir.mkdir(parents=True, exist_ok=True)
    promoted = 0

    for item in src_dir.iterdir():
        if item.is_file() and item.suffix in {".yml", ".yaml"}:
            dst = dst_dir / item.name
            shutil.copy2(item, dst)
            print(f"Promoted workflow: {item} -> {dst}")
            promoted += 1

    if promoted == 0:
        print("No staged workflow files found to promote")
    return promoted

def main():
    print("=== Unified Promotion Layer ===")
    promote_workflows()
    print("=== Promotion Complete ===")

if __name__ == "__main__":
    main()
