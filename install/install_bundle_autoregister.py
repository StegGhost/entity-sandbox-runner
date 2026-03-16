import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
BUNDLE_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = BUNDLE_ROOT / "payload"
RECEIPTS = ROOT / "evidence_plane" / "install_receipts"
PIPELINE_REGISTRY = ROOT / "observatory" / "pipeline_registry.json"


def discover_modules():
    modules = []
    if not PAYLOAD.exists():
        return modules
    for py in PAYLOAD.rglob("*.py"):
        rel = py.relative_to(PAYLOAD)
        module = ".".join(rel.with_suffix("").parts)
        modules.append({"file": str(rel), "module": module})
    return modules


def install_payload():
    installed = []
    for p in PAYLOAD.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(PAYLOAD)
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
        installed.append(str(dest))
        print(f"installed: {dest}")
    return installed


def update_registry(modules):
    if not PIPELINE_REGISTRY.exists():
        return
    try:
        data = json.loads(PIPELINE_REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        return

    if isinstance(data, dict) and "modules" in data and isinstance(data["modules"], list):
        existing = {m.get("module") if isinstance(m, dict) else m for m in data["modules"]}
        for module in modules:
            if module["module"] not in existing:
                data["modules"].append(module)
        PIPELINE_REGISTRY.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_receipt(installed, modules):
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    receipt = {
        "timestamp": datetime.utcnow().isoformat(),
        "bundle": BUNDLE_ROOT.name,
        "installed_files": installed,
        "modules_registered": modules,
    }
    (RECEIPTS / f"{BUNDLE_ROOT.name}_install_receipt.json").write_text(
        json.dumps(receipt, indent=2), encoding="utf-8"
    )


def main():
    modules = discover_modules()
    installed = install_payload()
    update_registry(modules)
    write_receipt(installed, modules)
    print(json.dumps({
        "installed_files": len(installed),
        "modules_registered": len(modules)
    }, indent=2))


if __name__ == "__main__":
    main()
