import os, zipfile, json, shutil, tempfile

REQUIRED_FIELDS = {
    "bundle_name": "unknown_bundle",
    "bundle_version": "0.0.0",
    "install_mode": "merge"
}

ALLOWED_ROOT_DIRS = ["payload", "install", "config", "experiments"]


def safe_json_load(path):
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except:
        return {}


def normalize_manifest(manifest):
    for k, default in REQUIRED_FIELDS.items():
        if k not in manifest:
            manifest[k] = default
    return manifest


def find_manifest(root):
    for r, _, files in os.walk(root):
        if "bundle_manifest.json" in files:
            return os.path.join(r, "bundle_manifest.json")
    return None


def ensure_structure(root):
    """
    If bundle dumped files at top-level, move into /payload
    """
    top_files = os.listdir(root)

    has_expected = any(d in top_files for d in ALLOWED_ROOT_DIRS)

    if not has_expected:
        payload_dir = os.path.join(root, "payload")
        os.makedirs(payload_dir, exist_ok=True)

        for item in top_files:
            src = os.path.join(root, item)
            if item == "payload":
                continue
            shutil.move(src, os.path.join(payload_dir, item))


def adapt_bundle(bundle_path):
    tmp_dir = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(bundle_path, 'r') as z:
            z.extractall(tmp_dir)

        # normalize structure first
        ensure_structure(tmp_dir)

        manifest_path = find_manifest(tmp_dir)

        if manifest_path:
            manifest = safe_json_load(manifest_path)
        else:
            manifest = {}

        manifest = normalize_manifest(manifest)

        # always rewrite manifest at root
        new_manifest_path = os.path.join(tmp_dir, "bundle_manifest.json")
        with open(new_manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        # rebuild zip
        new_zip_path = bundle_path + ".adapted.zip"

        with zipfile.ZipFile(new_zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    full = os.path.join(root, file)
                    rel = os.path.relpath(full, tmp_dir)
                    z.write(full, rel)

        shutil.move(new_zip_path, bundle_path)

        return True, "adapted"

    except Exception as e:
        return False, str(e)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
