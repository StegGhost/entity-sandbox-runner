import json
import os
import re
import shutil
import zipfile


def _safe_slug(value):
    value = (value or "untitled").strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "_", value)
    return value.strip("._-") or "untitled"


def build_bundle(topic, files, target="incoming_bundles"):
    slug = _safe_slug(topic)
    root = f"_tmp_bundle_{slug}"

    if os.path.exists(root):
        shutil.rmtree(root)

    for path, content in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)

    manifest = {
        "bundle_name": f"{slug}_bundle",
        "bundle_version": "1.0.0",
        "version": "1.0.0",
        "install_mode": "folder_map",
        "allowed_paths": ["payload/"]
    }

    with open(os.path.join(root, "bundle_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    os.makedirs(target, exist_ok=True)
    zip_path = os.path.join(target, f"{slug}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for r, _, fs in os.walk(root):
            for fn in fs:
                fp = os.path.join(r, fn)
                z.write(fp, os.path.relpath(fp, root))

    return zip_path
