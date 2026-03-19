import os, json, zipfile

def build_bundle(topic, files, target="incoming_bundles"):
    root = f"_tmp_bundle_{topic}"

    for path, content in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)

    manifest = {
        "bundle_name": f"{topic}_bundle",
        "bundle_version": "1.0.0",
        "version": "1.0.0",
        "install_mode": "folder_map",
        "allowed_paths": ["payload/"]
    }

    with open(os.path.join(root, "bundle_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    os.makedirs(target, exist_ok=True)

    zip_path = os.path.join(target, f"{topic}.zip")

    with zipfile.ZipFile(zip_path, "w") as z:
        for r, _, files in os.walk(root):
            for f in files:
                fp = os.path.join(r, f)
                z.write(fp, os.path.relpath(fp, root))

    return zip_path
