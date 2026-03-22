import json
import shutil
import zipfile
from pathlib import Path


def proposal_to_bundle(proposal, output_path="incoming_bundles/auto_bundle_feedback.zip"):
    temp_dir = Path("tmp_bundle_feedback")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    install_dir = temp_dir / "install"
    install_dir.mkdir(parents=True, exist_ok=True)

    for f in proposal.get("files_to_create", []):
        rel = Path(f["path"])
        if rel.parts[0] != "install":
            raise ValueError("files_to_create paths must start with install/")
        path = temp_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f["content"], encoding="utf-8")

    manifest = {
        "bundle_name": "auto_generated_feedback_bundle",
        "bundle_version": "1.0.0",
        "version": "1.0.0",
        "install_mode": "folder_map",
        "allowed_paths": [
            "bundle_manifest.json",
            "install/tests/",
            "install/engine/"
        ]
    }

    (temp_dir / "bundle_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    Path("incoming_bundles").mkdir(exist_ok=True)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in temp_dir.rglob("*"):
            z.write(p, p.relative_to(temp_dir))

    return output_path
