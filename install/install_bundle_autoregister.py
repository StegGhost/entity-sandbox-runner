import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
BUNDLE_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = BUNDLE_ROOT / "payload"
RECEIPTS = ROOT / "evidence_plane" / "install_receipts"


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


def try_run(script_rel: str):
    script = ROOT / script_rel
    if not script.exists():
        return {"script": script_rel, "ran": False, "reason": "missing"}

    try:
        subprocess.run([sys.executable, str(script)], cwd=ROOT, check=False)
        return {"script": script_rel, "ran": True, "reason": "ok"}
    except Exception as e:
        return {"script": script_rel, "ran": False, "reason": repr(e)}


def refresh_pipeline():
    actions = []
    actions.append(try_run("observatory/discover_pipeline_plugins.py"))
    actions.append(try_run("observatory/build_pipeline_registry.py"))
    actions.append(try_run("observatory/build_pipeline_dag.py"))
    return actions


def write_receipt(installed, refresh_actions):
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    receipt = {
        "bundle": BUNDLE_ROOT.name,
        "installed_files": installed,
        "refresh_actions": refresh_actions,
    }
    receipt_path = RECEIPTS / "bundle_install_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"receipt: {receipt_path}")


def main():
    installed = install_payload()
    refresh_actions = refresh_pipeline()
    write_receipt(installed, refresh_actions)
    print(json.dumps({
        "installed_files": len(installed),
        "refresh_actions": refresh_actions,
    }, indent=2))


if __name__ == "__main__":
    main()
