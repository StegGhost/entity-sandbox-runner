import os
import json
import argparse
import zipfile
import time
from typing import Dict, Any

ROOT = os.getcwd()

REPORT_DIR = os.path.join(ROOT, "brain_reports")
os.makedirs(REPORT_DIR, exist_ok=True)


def now_ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def load_action_payload(payload_str: str) -> Dict[str, Any]:
    try:
        return json.loads(payload_str)
    except Exception:
        return {}


def validate_zip_structure(zip_path: str) -> Dict[str, Any]:
    result = {
        "valid_zip": False,
        "manifest_present": False,
        "install_dir_present": False,
        "files": []
    }

    if not zipfile.is_zipfile(zip_path):
        return result

    result["valid_zip"] = True

    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            names = z.namelist()
            result["files"] = names

            # Normalize paths
            normalized = [n.strip("/") for n in names]

            result["manifest_present"] = any(
                n.endswith("bundle_manifest.json") for n in normalized
            )

            result["install_dir_present"] = any(
                n.startswith("install/") or "/install/" in n for n in normalized
            )

    except Exception:
        pass

    return result


def determine_action(validation: Dict[str, Any]) -> str:
    if not validation["valid_zip"]:
        return "reject_invalid_zip"

    if not validation["manifest_present"]:
        return "reject_missing_manifest"

    if not validation["install_dir_present"]:
        return "reject_missing_install"

    return "promote_to_install"


def inspect_bundle(action_payload: Dict[str, Any]) -> Dict[str, Any]:
    ts = now_ts()

    target = action_payload.get("target")
    family = action_payload.get("family", "unknown")

    if not target or not os.path.exists(target):
        return {
            "status": "failed",
            "reason": "target_not_found",
            "target": target,
            "ts": ts
        }

    validation = validate_zip_structure(target)
    action = determine_action(validation)

    result = {
        "status": "ok",
        "ts": ts,
        "target": target,
        "family": family,
        "validation": validation,
        "decision": {
            "action": action,
            "valid": action == "promote_to_install"
        }
    }

    return result


def write_report(result: Dict[str, Any]) -> str:
    path = os.path.join(REPORT_DIR, "inspection_result.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-payload-json", required=True)
    args = parser.parse_args()

    payload = load_action_payload(args.action_payload_json)

    result = inspect_bundle(payload)
    output_path = write_report(result)

    print(json.dumps({
        "status": "ok",
        "output": output_path,
        "inspection": result
    }, indent=2))


if __name__ == "__main__":
    main()
