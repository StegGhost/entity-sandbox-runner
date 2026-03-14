import zipfile
import shutil
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
REPORT_DIR = ROOT / "ingestion_reports"
REPORT_DIR.mkdir(exist_ok=True)

TARGET_MAP = {
    "runner": "runner",
    "observatory": "observatory",
    "multi_entity_sim": "multi_entity_sim",
    "interaction_graph": "interaction_graph",
    "adaptive_scanner": "adaptive_scanner",
    "statistics": "statistics",
    "reproducibility": "reproducibility",
    "visualization": "visualization",
    "sandbox": "sandbox",
    "sdk": "sdk",
    "experiments": "experiments",
    "entities": "entities",
    "ingestion": "ingestion",
    ".github": ".github"
}

def log(msg):
    ts = datetime.utcnow().isoformat()
    with open(REPORT_DIR / "ingestion.log", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg)

def extract_if_zip(path):
    p = Path(path)
    if p.suffix != ".zip":
        return p

    tmp = ROOT / "ingestion_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(p) as z:
        z.extractall(tmp)

    return tmp

def backup_file(dest):
    if not dest.exists():
        return
    backup_dir = ROOT / "ingestion_backup"
    backup_dir.mkdir(exist_ok=True)
    backup_target = backup_dir / dest.name
    shutil.copy2(dest, backup_target)

def merge_tree(src, dest):
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        backup_file(target)
        shutil.copy2(item, target)
        log(f"installed {target}")

def ingest(path):
    src = extract_if_zip(path)

    matched = 0
    for name, target in TARGET_MAP.items():
        found = list(src.rglob(name))
        for f in found:
            dest = ROOT / target
            log(f"merging {f} -> {dest}")
            merge_tree(f, dest)
            matched += 1

    if matched == 0:
        # fallback: merge entire extracted tree into repo root except the top folder itself
        top_entries = [p for p in src.iterdir()]
        for entry in top_entries:
            if entry.is_file():
                target = ROOT / entry.name
                backup_file(target)
                shutil.copy2(entry, target)
                log(f"installed {target}")
            else:
                merge_tree(entry, ROOT / entry.name)
                matched += 1

    log(f"ingestion complete; matched modules={matched}")

def main():
    if len(sys.argv) < 2:
        print("usage: python ingestion/ingest_bundle.py <bundle_or_directory>")
        sys.exit(1)

    ingest(sys.argv[1])

if __name__ == "__main__":
    main()
