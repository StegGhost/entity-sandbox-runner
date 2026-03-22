from pathlib import Path
import shutil

ROOT = Path.cwd()
SRC = ROOT / "install"

def move_tree(src: Path, dest: Path):
    if not src.exists():
        return
    for p in src.rglob("*"):
        if p.is_file():
            rel = p.relative_to(src)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)

move_tree(SRC / "engine", ROOT / "engine")
move_tree(SRC / "tests", ROOT / "tests")
print("apply.py executed")
