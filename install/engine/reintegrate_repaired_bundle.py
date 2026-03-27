import os
import shutil
import json
import subprocess
from typing import Dict, Any

ROOT = os.getcwd()

FAILED_DIR = os.path.join(ROOT, "failed_bundles")
INCOMING_DIR = os.path.join(ROOT, "incoming_bundles")
REPAIRED_DIR = os.path.join(ROOT, "repaired_bundles")


def reintegrate(action_payload: Dict[str, Any]) -> Dict[str, Any]:
    repaired_bundle = action_payload.get("repaired_bundle")

    if not repaired_bundle or not os.path.exists(repaired_bundle):
        return {"status": "failed", "reason": "missing_repaired_bundle"}

    bundle_name = os.path.basename(repaired_bundle)
    incoming_path = os.path.join(INCOMING_DIR, bundle_name)

    os.makedirs(INCOMING_DIR, exist_ok=True)

    # Step 1: move to incoming
    shutil.copy(repaired_bundle, incoming_path)

    # Step 2: trigger ingestion
    try:
        result = subprocess.run(
            ["python", "install/ingestion_v2.py", "--bundle", incoming_path],
            capture_output=True,
            text=True
        )

        success = result.returncode == 0

    except Exception as e:
        return {
            "status": "failed",
            "reason": "ingestion_error",
            "error": str(e)
        }

    # Step 3: if success → clean up failed bundle
    original_failed = os.path.join(FAILED_DIR, bundle_name)

    if success and os.path.exists(original_failed):
        os.remove(original_failed)

    return {
        "status": "ok" if success else "failed",
        "reintegrated": success,
        "incoming_path": incoming_path,
        "original_failed_removed": success,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
