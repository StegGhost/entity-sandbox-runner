import os
import json
import uuid
from datetime import datetime


def proposal_to_bundle(proposal: dict):
    """
    Converts a proposal into a bundle on disk.
    """

    bundle_id = f"bundle_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:6]}"
    base_path = os.path.join("incoming_bundles", bundle_id)

    os.makedirs(base_path, exist_ok=True)

    files = proposal.get("files_to_create", [])

    written_files = []

    for file in files:
        path = file.get("path")
        content = file.get("content", "")

        if not path:
            continue

        full_path = os.path.join(base_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)

        written_files.append(path)

    manifest = {
        "bundle_id": bundle_id,
        "proposal_name": proposal.get("proposal_name"),
        "created_at": datetime.utcnow().isoformat(),
        "files": written_files,
    }

    with open(os.path.join(base_path, "bundle_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    return {
        "status": "bundle_created",
        "bundle_id": bundle_id,
        "path": base_path,
        "files_written": written_files,
    }
