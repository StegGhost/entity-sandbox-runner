
from pathlib import Path
import shutil

ROOT = Path.cwd()
SRC = ROOT / "install"

def move(src, dst):
    if not src.exists(): return
    for p in src.rglob("*"):
        if p.is_file():
            t = dst / p.relative_to(src)
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t)

move(SRC/"engine", ROOT/"engine")
move(SRC/"tests", ROOT/"tests")
print("slashing + rewards installed")
