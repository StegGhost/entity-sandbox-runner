import os
import json
from datetime import datetime

ROOT = os.getcwd()

DIRS = {
    "failed": "failed_bundles",
    "incoming": "incoming_bundles",
    "installed": "installed_bundles"
}

OUTPUT_DIR = os.path.join(ROOT, "brain_reports")
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "bundle_inventory.json")
OUTPUT_MD = os.path.join(OUTPUT_DIR, "bundle_inventory.md")


def scan():
    inventory = {}

    for key, rel in DIRS.items():
        full = os.path.join(ROOT, rel)
        files = []

        if os.path.exists(full):
            for f in sorted(os.listdir(full)):
                files.append(f)

        inventory[key] = files

    return inventory


def write_outputs(inventory):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat(),
            "inventory": inventory
        }, f, indent=2)

    # Markdown (human readable)
    lines = ["# Bundle Inventory\n"]

    for section, files in inventory.items():
        lines.append(f"## {section.upper()}\n")
        for f in files:
            lines.append(f"- {f}")
        lines.append("")

    with open(OUTPUT_MD, "w") as f:
        f.write("\n".join(lines))


def main():
    inventory = scan()
    write_outputs(inventory)

    print(json.dumps({
        "status": "ok",
        "sections": list(inventory.keys())
    }, indent=2))


if __name__ == "__main__":
    main()
