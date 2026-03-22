from pathlib import Path
import shutil

ROOT = Path.cwd()
SRC = ROOT / "install"

def move(src, dst):
    for p in src.rglob("*"):
        if p.is_file():
            rel = p.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)

move(SRC / "engine", ROOT / "engine")
move(SRC / "tests", ROOT / "tests")
print("apply.py executed")
