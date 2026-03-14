import json
from pathlib import Path
from datetime import datetime


def build_handoff_manifest(exp_path, result):

    manifest = {
        "experiment_id": exp_path.name,
        "timestamp": datetime.utcnow().isoformat(),
        "entities": ["sandbox_A"],
        "proposal_count": len(result["receipts"]),
        "result_file": f"results/{exp_path.name}_results.json",
    }

    manifests = Path("manifests")
    manifests.mkdir(exist_ok=True)

    out = manifests / f"{exp_path.name}_handoff.json"

    with open(out, "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest
