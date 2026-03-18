import os, zipfile, shutil, json, hashlib, time
from install.compat_adapter import adapt_bundle

INCOMING = "incoming_bundles"
INSTALLED = "installed_bundles"
FAILED = "failed_bundles"
TMP = "_ingest_tmp"

REQUIRED_MANIFEST_FIELDS = [
    "bundle_name",
    "bundle_version",
    "install_mode"
]

def safe_json_load(path):
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except Exception:
        return {}

def ensure_dirs():
    for d in [INCOMING, INSTALLED, FAILED, TMP]:
        os.makedirs(d, exist_ok=True)

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def validate_manifest(manifest):
    for k in REQUIRED_MANIFEST_FIELDS:
        if k not in manifest:
            return False, f"missing_{k}"
    return True, "ok"

def install_files(src_root):
    for root, _, files in os.walk(src_root):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, src_root)

            if rel.startswith("payload/") or rel.startswith("install/") or rel.startswith("config/") or rel.startswith("experiments/"):
                dest = rel
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(full, dest)

def process_bundle(bundle_path):
    bundle_name = os.path.basename(bundle_path)
    tmp_dir = os.path.join(TMP, bundle_name)

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    os.makedirs(tmp_dir, exist_ok=True)

    try:
        # attempt compatibility adaptation first
      adapt_ok, _ = adapt_bundle(bundle_path)

      with zipfile.ZipFile(bundle_path, 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)

        manifest_path = None
        for root, _, files in os.walk(tmp_dir):
            if "bundle_manifest.json" in files:
                manifest_path = os.path.join(root, "bundle_manifest.json")
                break

        if not manifest_path:
            return False, "no_manifest"

        manifest = safe_json_load(manifest_path)

        valid, reason = validate_manifest(manifest)
        if not valid:
            return False, reason

        install_files(tmp_dir)

        return True, "installed"

    except Exception as e:
        return False, str(e)

def move_bundle(src, success):
    dest_dir = INSTALLED if success else FAILED
    os.makedirs(dest_dir, exist_ok=True)
    shutil.move(src, os.path.join(dest_dir, os.path.basename(src)))

def run():
    ensure_dirs()

    bundles = sorted([
        os.path.join(INCOMING, f)
        for f in os.listdir(INCOMING)
        if f.endswith(".zip")
    ])

    results = []

    for b in bundles:
        ok, reason = process_bundle(b)
        move_bundle(b, ok)
        results.append({
            "bundle": os.path.basename(b),
            "status": "installed" if ok else "failed",
            "reason": reason
        })

    print("INGESTION RESULTS:", results)
    return results

if __name__ == "__main__":
    run()
