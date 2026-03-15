from pathlib import Path
import shutil

ROOT = Path.cwd()
PAYLOAD = ROOT / "payload"

TARGETS = [
    "control_plane",
    "security_plane",
    "evidence_plane",
    "observatory",
]

def copy_tree(src: Path, dst: Path):
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        out = dst / rel
        if p.is_dir():
            out.mkdir(parents=True, exist_ok=True)
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, out)

def main():
    if not PAYLOAD.exists():
        raise RuntimeError(f"missing payload directory: {PAYLOAD}")

    for name in TARGETS:
        src = PAYLOAD / name
        if not src.exists():
            continue
        dst = ROOT / name
        copy_tree(src, dst)
        print(f"installed {name} -> {dst}")

if __name__ == "__main__":
    main()
