from pathlib import Path
import shutil
import hashlib
import json
from datetime import datetime

ROOT = Path.cwd()
PAYLOAD = ROOT / "payload"
LEDGER = ROOT / "observatory" / "state_log" / "runtime_ledger.jsonl"
RECEIPTS = ROOT / "receipts"

TARGETS = [
    "control_plane",
    "security_plane",
    "evidence_plane",
    "observatory"
]


def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def copy_tree(src: Path, dst: Path):
    installed = []
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        out = dst / rel

        if p.is_dir():
            out.mkdir(parents=True, exist_ok=True)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, out)
            installed.append(out)

    return installed


def verify_tvc():
    tvc = ROOT / "payload/control_plane/tvc/verify_bundle_install.py"
    if tvc.exists():
        exec(tvc.read_text(), {})


def write_receipt(files):
    RECEIPTS.mkdir(exist_ok=True)

    receipt = {
        "timestamp": datetime.utcnow().isoformat(),
        "files": {}
    }

    for f in files:
        receipt["files"][str(f)] = hash_file(f)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out = RECEIPTS / f"install_receipt_{ts}.json"

    with open(out, "w") as f:
        json.dump(receipt, f, indent=2)

    return out


def append_ledger(receipt_path):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "receipt": str(receipt_path)
    }

    LEDGER.parent.mkdir(parents=True, exist_ok=True)

    with open(LEDGER, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    if not PAYLOAD.exists():
        raise RuntimeError("payload directory missing")

    verify_tvc()

    installed_files = []

    for name in TARGETS:
        src = PAYLOAD / name
        if not src.exists():
            continue

        dst = ROOT / name
        files = copy_tree(src, dst)
        installed_files.extend(files)

        print(f"installed {name}")

    receipt = write_receipt(installed_files)
    append_ledger(receipt)

    print("promotion complete")
    print(f"receipt: {receipt}")


if __name__ == "__main__":
    main()
