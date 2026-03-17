
import shutil
from pathlib import Path

ROOT = Path.cwd()
BUNDLE_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = BUNDLE_ROOT / "payload"

def main():
    for p in PAYLOAD.rglob("*"):
        if p.is_file():
            dest = ROOT / p.relative_to(PAYLOAD)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
            print("installed", dest)

if __name__ == "__main__":
    main()
