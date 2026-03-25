import os
import json
import shutil
import zipfile
import tempfile
from pathlib import Path

# ==============================
# CONFIG
# ==============================

STAGING_PREFIX = "bundle_build_"
OUTPUT_DIR = "outgoing_bundles"

# ==============================
# UTIL
# ==============================

def normalize_path(p: str) -> str:
    return p.replace("\\", "/").lstrip("./")

def is_path_allowed(path: str, allowed_paths: list[str]) -> bool:
    path = normalize_path(path)

    for allowed in allowed_paths:
        allowed = normalize_path(allowed)

        # directory
        if allowed.endswith("/"):
            if path.startswith(allowed):
                return True

        # exact file
        if path == allowed:
            return True

    return False


def list_all_files(root: Path):
    files = []
    for p in root.rglob("*"):
        if p.is_file():
            files.append(normalize_path(str(p.relative_to(root))))
    return files


# ==============================
# CORE BUILDER
# ==============================

def build_bundle(bundle_name: str, bundle_version: str, manifest: dict, file_map: dict):
    """
    file_map: {
        "source/absolute/or/relative/path": "target/path/in/bundle"
    }
    """

    # ------------------------------
    # 1. Create sterile staging dir
    # ------------------------------
    staging_dir = Path(tempfile.mkdtemp(prefix=STAGING_PREFIX))

    try:
        # ------------------------------
        # 2. Write manifest (normalized)
        # ------------------------------
        allowed_paths = manifest.get("allowed_paths", [])
        allowed_paths = [normalize_path(p.rstrip("/") + "/" if p.endswith("/") else p) for p in allowed_paths]

        manifest["allowed_paths"] = allowed_paths

        manifest_path = staging_dir / "bundle_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        # ------------------------------
        # 3. Copy ONLY whitelisted files
        # ------------------------------
        provenance = []

        for src, dst in file_map.items():
            src_path = Path(src)
            dst_path = staging_dir / normalize_path(dst)

            if not src_path.exists():
                raise Exception(f"[BUILD ERROR] Missing source file: {src}")

            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)

            provenance.append({
                "source": str(src_path),
                "target": str(dst_path.relative_to(staging_dir))
            })

        # ------------------------------
        # 4. Pre-zip validation
        # ------------------------------
        all_files = list_all_files(staging_dir)

        violations = []
        for f in all_files:
            if not is_path_allowed(f, allowed_paths):
                violations.append(f)

        if violations:
            raise Exception(json.dumps({
                "error": "bundle_self_audit_failed",
                "violations": violations,
                "allowed_paths": allowed_paths,
                "files": all_files
            }, indent=2))

        # ------------------------------
        # 5. Write provenance log
        # ------------------------------
        with open(staging_dir / "build_provenance.json", "w") as f:
            json.dump(provenance, f, indent=2)

        # ------------------------------
        # 6. Zip ONLY staging dir
        # ------------------------------
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        bundle_filename = f"{bundle_name}_{bundle_version}.zip"
        bundle_path = Path(OUTPUT_DIR) / bundle_filename

        with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as z:
            for file in staging_dir.rglob("*"):
                if file.is_file():
                    z.write(file, file.relative_to(staging_dir))

        print(f"[SUCCESS] Bundle built: {bundle_path}")
        return str(bundle_path)

    finally:
        # ------------------------------
        # 7. Hard cleanup (no leakage)
        # ------------------------------
        shutil.rmtree(staging_dir, ignore_errors=True)


# ==============================
# SAFE ENTRYPOINT
# ==============================

def generate_bundle(proposal: dict):
    """
    Expected proposal format:
    {
        "bundle_name": str,
        "bundle_version": str,
        "manifest": {...},
        "files": {
            "src_path": "dst_path"
        }
    }
    """

    required = ["bundle_name", "bundle_version", "manifest", "files"]
    for r in required:
        if r not in proposal:
            raise Exception(f"[INVALID PROPOSAL] Missing: {r}")

    return build_bundle(
        proposal["bundle_name"],
        proposal["bundle_version"],
        proposal["manifest"],
        proposal["files"]
    )
