import os
import json
import shutil
from datetime import datetime

OUTPUT_DIR = "incoming_bundles"
REPORT_PATH = "brain_reports/repair_report.json"


def _write_report(data):
    os.makedirs("brain_reports", exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(data, f, indent=2)


def _sanitize_bundle(bundle_path):
    """
    Minimal repair strategy:
    - remove disallowed paths (e.g., docs/)
    - keep only admissible install/ structure
    """

    if not os.path.exists(bundle_path):
        return None, "bundle_not_found"

    repaired_path = bundle_path.replace(".zip", "_repaired.zip")

    # --- TEMP DIR ---
    tmp_dir = bundle_path + "_tmp"

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    os.makedirs(tmp_dir, exist_ok=True)

    # --- UNZIP ---
    shutil.unpack_archive(bundle_path, tmp_dir)

    # --- REMOVE DISALLOWED PATHS ---
    for root, dirs, files in os.walk(tmp_dir):
        for d in list(dirs):
            if d == "docs":
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)

    # --- REPACK ---
    shutil.make_archive(repaired_path.replace(".zip", ""), 'zip', tmp_dir)

    shutil.rmtree(tmp_dir)

    return repaired_path, None


def propose_repair(action_payload):
    ts = datetime.utcnow().isoformat()

    target = action_payload.get("target")

    if not target:
        report = {
            "status": "failed",
            "reason": "no_target_bundle",
            "ts": ts
        }
        _write_report(report)
        return report

    repaired_bundle, err = _sanitize_bundle(target)

    if err:
        report = {
            "status": "failed",
            "reason": err,
            "target": target,
            "ts": ts
        }
        _write_report(report)
        return report

    # --- MOVE TO INCOMING ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    final_path = os.path.join(
        OUTPUT_DIR,
        os.path.basename(repaired_bundle)
    )

    shutil.move(repaired_bundle, final_path)

    report = {
        "status": "ok",
        "action": "repair_generated",
        "original_bundle": target,
        "repaired_bundle": final_path,
        "ts": ts
    }

    _write_report(report)
    return report
