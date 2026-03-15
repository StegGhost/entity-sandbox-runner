from pathlib import Path
import shutil

ROOT = Path.cwd()
PAYLOAD = ROOT / "payload"

TARGETS = [
    ("evidence_plane", ["ledger", "replay"]),
    ("observatory", ["state_log"]),
    ("security_plane", ["integrity"]),
]

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
            installed.append(str(out))
    return installed

def main():
    if not PAYLOAD.exists():
        raise RuntimeError(f"missing payload directory: {PAYLOAD}")

    installed = []
    for top, children in TARGETS:
        for child in children:
            src = PAYLOAD / top / child
            if not src.exists():
                continue
            dst = ROOT / top / child
            installed.extend(copy_tree(src, dst))
            print(f"installed {src} -> {dst}")

    print("runtime ledger promotion complete")
    print(f"installed_files={len(installed)}")

if __name__ == "__main__":
    main()
