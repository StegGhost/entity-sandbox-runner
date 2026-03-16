
import shutil
from pathlib import Path

ROOT = Path.cwd()
BUNDLE_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = BUNDLE_ROOT / "payload"

def install_payload():
    for p in PAYLOAD.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(PAYLOAD)
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
        print("installed:", dest)

def main():
    install_payload()

if __name__ == "__main__":
    main()
