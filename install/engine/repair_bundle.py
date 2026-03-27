import os
import json
import zipfile
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FAILED_DIR = ROOT / "failed_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"
TMP_DIR = ROOT / "_repair_tmp"
REPORT_PATH = ROOT / "brain_reports" / "repair_bundle_result.json"


def now():
    return datetime.utcnow().isoformat() + "Z"


def sha256_file(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def ensure_dirs():
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    REPAIRED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)


def unzip_bundle(bundle_path: Path, extract_to: Path):
    if extract_to.exists():
        shutil.rmtree(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(bundle_path, "r") as z:
        z.extractall(extract_to)


def zip_bundle(folder_path: Path, output_path: Path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full = Path(root) / file
                rel = full.relative_to(folder_path)
                z.write(full, str(rel))


def load_manifest(root: Path):
    manifest_path = root / "bundle_manifest.json"
    if not manifest_path.exists():
        return None, manifest_path

    try:
        return json.loads(manifest_path.read_text(encoding="utf-8")), manifest_path
    except Exception:
        return None, manifest_path


def write_manifest(manifest_path: Path, data: dict):
    manifest_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def fix_manifest(manifest: dict, bundle_stem: str):
    changed = False

    required_defaults = {
        "bundle_name": bundle_stem,
        "bundle_version": "0.0.1",
        "status": "repaired",
        "capabilities": {},
        "files": []
    }

    for key, default in required_defaults.items():
        if key not in manifest:
            manifest[key] = default
            changed = True

    return manifest, changed


def derive_family(bundle_name: str):
    if not bundle_name:
        return "unknown"
    parts = bundle_name.split("_")
    return "_".join(parts[:3]) if len(parts) >= 3 else bundle_name


def ensure_install_stub(root: Path):
    install_dir = root / "install"
    apply_py = install_dir / "apply.py"

    if apply_py.exists():
        return False

    install_dir.mkdir(parents=True, exist_ok=True)
    apply_py.write_text(
        'print("auto repaired bundle executed")\n',
        encoding="utf-8"
    )
    return True


def refresh_manifest_files(manifest: dict, root: Path):
    files = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            files.append(str(path.relative_to(root)))
    manifest["files"] = files
    return manifest


def repair_bundle(bundle_path: Path):
    ensure_dirs()

    bundle_name = bundle_path.name
    bundle_stem = bundle_path.stem
    tmp_extract = TMP_DIR / bundle_stem

    result = {
        "ts": now(),
        "status": "failed",
        "input_bundle": str(bundle_path),
        "output_bundle": None,
        "changes_applied": [],
        "errors": [],
        "family": None,
        "hash_before": None,
        "hash_after": None
    }

    try:
        result["hash_before"] = sha256_file(bundle_path)

        unzip_bundle(bundle_path, tmp_extract)

        manifest, manifest_path = load_manifest(tmp_extract)

        if manifest is None:
            manifest = {
                "bundle_name": bundle_stem,
                "bundle_version": "0.0.1",
                "status": "repaired",
                "capabilities": {},
                "files": []
            }
            write_manifest(manifest_path, manifest)
            result["changes_applied"].append("created_missing_manifest")
        else:
            manifest, changed = fix_manifest(manifest, bundle_stem)
            if changed:
                write_manifest(manifest_path, manifest)
                result["changes_applied"].append("fixed_manifest_fields")

        if ensure_install_stub(tmp_extract):
            result["changes_applied"].append("created_missing_install_stub")

        manifest = manifest or {}
        manifest, _ = fix_manifest(manifest, bundle_stem)
        manifest = refresh_manifest_files(manifest, tmp_extract)
        write_manifest(manifest_path, manifest)

        result["family"] = derive_family(manifest.get("bundle_name"))

        repaired_path = REPAIRED_DIR / bundle_name
        zip_bundle(tmp_extract, repaired_path)

        result["output_bundle"] = str(repaired_path)
        result["hash_after"] = sha256_file(repaired_path)
        result["status"] = "repaired"

    except Exception as e:
        result["errors"].append(str(e))

    finally:
        if tmp_extract.exists():
            shutil.rmtree(tmp_extract)

    REPORT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps({
        "status": result["status"],
        "output": str(REPORT_PATH),
        "result": result
    }))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Path to failed bundle zip")
    args = parser.parse_args()

    repair_bundle(Path(args.target))
