import io
import json
import os
import zipfile
from datetime import datetime
from pathlib import Path


def proposal_to_bundle(proposal: dict, output_path: str = "incoming_bundles/auto_bundle_feedback.zip"):
    """
    Convert a proposal into a real zip bundle for ingestion.

    Expected proposal shape:
    {
      "proposal_name": "...",
      "files_to_create": [
        {"path": "install/foo.py", "content": "..."}
      ]
    }
    """

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    files = proposal.get("files_to_create", [])
    normalized_files = []

    for item in files:
        rel_path = item.get("path")
        content = item.get("content", "")
        if not rel_path:
            continue
        normalized_files.append({
            "path": rel_path.replace("\\", "/"),
            "content": content,
        })

    manifest = {
        "bundle_name": proposal.get("proposal_name", "auto_bundle_feedback"),
        "bundle_version": "1.0.0",
        "install_mode": "folder_map",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": [f["path"] for f in normalized_files],
    }

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("bundle_manifest.json", json.dumps(manifest, indent=2) + "\n")

        for item in normalized_files:
            zf.writestr(item["path"], item["content"])

    return {
        "status": "bundle_created",
        "output_path": str(output),
        "bundle_name": manifest["bundle_name"],
        "bundle_version": manifest["bundle_version"],
        "files_written": manifest["files"],
    }
