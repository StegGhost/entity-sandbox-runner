import os
import json
import shutil
import time
from typing import Dict, Any

ROOT = os.getcwd()

FAILED_DIR = os.path.join(ROOT, "failed_bundles")
INCOMING_DIR = os.path.join(ROOT, "incoming_bundles")
REPAIRED_DIR = os.path.join(ROOT, "repaired_bundles")

os.makedirs(REPAIRED_DIR, exist_ok=True)


def resolve_bundle_path(target: str) -> str:
    """
    Resolve bundle location across possible directories.
    """

    # If already absolute or relative with folder
    if os.path.exists(target):
        return target

    # Check failed_bundles
    failed_path = os.path.join(FAILED_DIR, target)
    if os.path.exists(failed_path):
        return failed_path

    # Check incoming_bundles
    incoming_path = os.path.join(INCOMING_DIR, target)
    if os.path.exists(incoming_path):
        return incoming_path

    return ""


def propose_repair(action_payload: Dict[str, Any]) -> Dict[str, Any]:
    ts = time.strftime("%Y%m%d_%H%M%S")

    target = action_payload.get("target")
    family = action_payload.get("family", "unknown")

    if not target:
        return {
            "status": "failed",
            "reason": "missing_target"
        }

    resolved_path = resolve_bundle_path(target)

    if not resolved_path:
        return {
            "status": "failed",
            "reason": "bundle_not_found",
            "target": target
        }

    bundle_name = os.path.basename(resolved_path)

    repaired_name = bundle_name.replace(".zip", f"_repaired_{ts}.zip")
    repaired_path = os.path.join(REPAIRED_DIR, repaired_name)

    try:
        shutil.copy(resolved_path, repaired_path)
    except Exception as e:
        return {
            "status": "failed",
            "reason": "copy_failed",
            "error": str(e)
        }

    return {
        "status": "ok",
        "family": family,
        "original_bundle": resolved_path,
        "repaired_bundle": repaired_path,
        "ts": ts
    }
