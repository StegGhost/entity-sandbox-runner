import zipfile
import shutil
import sys
import json
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
REPORT_DIR = ROOT / "ingestion_reports"
REPORT_DIR.mkdir(exist_ok=True)

FALLBACK_TARGET_MAP = {
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
    ".github": ".github",
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

    rel_name = dest.name
    target = backup_dir / rel_name
    counter = 1
    while target.exists():
        target = backup_dir / f"{dest.stem}_{counter}{dest.suffix}"
        counter += 1
    shutil.copy2(dest, target)

def copy_one(src: Path, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    backup_file(dest)
    shutil.copy2(src, dest)
    log(f"installed {dest}")

def merge_tree(src: Path, dest: Path):
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        copy_one(item, dest / rel)

def load_manifest(extracted_root: Path):
    manifests = list(extracted_root.rglob("bundle_manifest.json"))
    if not manifests:
        return None, None
    manifest_path = manifests[0]
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    return manifest_path, data

def install_from_manifest(extracted_root: Path, manifest_path: Path, manifest: dict):
    mode = manifest["install_mode"]
    base_dir = manifest_path.parent

    if mode == "file_map":
        mappings = manifest.get("file_map", {})
        for src_rel, dest_rel in mappings.items():
            src = base_dir / src_rel
            dest = ROOT / dest_rel
            if not src.exists():
                log(f"manifest source missing: {src}")
                continue
            copy_one(src, dest)
        return True

    if mode == "folder_map":
        mappings = manifest.get("folder_map", {})
        for src_rel, dest_rel in mappings.items():
            src = base_dir / src_rel
            dest = ROOT / dest_rel
            if not src.exists():
                log(f"manifest folder missing: {src}")
                continue
            log(f"manifest merge {src} -> {dest}")
            merge_tree(src, dest)
        return True

    return False

def install_fallback(extracted_root: Path):
    matched = 0
    for name, target in FALLBACK_TARGET_MAP.items():
        found = list(extracted_root.rglob(name))
        for f in found:
            dest = ROOT / target
            log(f"fallback merge {f} -> {dest}")
            merge_tree(f, dest)
            matched += 1

    if matched == 0:
        top_entries = [p for p in extracted_root.iterdir()]
        for entry in top_entries:
            if entry.is_file():
                copy_one(entry, ROOT / entry.name)
            else:
                merge_tree(entry, ROOT / entry.name)

    log(f"fallback ingestion complete; matched modules={matched}")

def ingest(path):
    extracted = extract_if_zip(path)

    manifest_path, manifest = load_manifest(extracted)
    if manifest is not None:
        log(f"using bundle manifest: {manifest_path}")
        ok = install_from_manifest(extracted, manifest_path, manifest)
        if ok:
            log("manifest-driven ingestion complete")
            return

    log("no valid manifest found; using fallback folder matching")
    install_fallback(extracted)

def main():
    if len(sys.argv) < 2:
        print("usage: python ingestion/ingest_bundle.py <bundle_or_directory>")
        raise SystemExit(1)

    ingest(sys.argv[1])

if __name__ == "__main__":
    main()
