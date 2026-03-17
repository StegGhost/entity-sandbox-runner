#!/usr/bin/env python3

import os
import shutil

def promote_workflows():
    src_dir = "payload/workflows"
    dst_dir = ".github/workflows"

    if not os.path.exists(src_dir):
        print("No workflow payload found")
        return

    os.makedirs(dst_dir, exist_ok=True)

    for file in os.listdir(src_dir):
        if file.endswith(".yml") or file.endswith(".yaml"):
            src = os.path.join(src_dir, file)
            dst = os.path.join(dst_dir, file)
            shutil.copy2(src, dst)
            print(f"Promoted workflow: {file}")

def main():
    print("=== Unified Promotion Layer ===")
    promote_workflows()
    print("=== Promotion Complete ===")

if __name__ == "__main__":
    main()
