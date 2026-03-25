import os
import json
import shutil
import zipfile
import tempfile
import subprocess
from datetime import datetime

ROOT = os.getcwd()
BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")
FAILED_BUNDLES = os.path.join(ROOT, "failed_bundles")
INCOMING_BUNDLES = os.path.join(ROOT, "incoming_bundles")
OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")
NEXT_ACTION_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")


def utc_now():
    return datetime.utcnow().isoformat()


def load_json(path, default=None):
    if default is None:
        default = {}
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_json(path, payload):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def default_allowed_paths_from_tree(extract_root):
    allowed = []
    for root, _, files in os.walk(extract_root):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, extract_root).replace("\\", "/")

            if rel == "bundle_manifest.json":
                if "bundle_manifest.json" not in allowed:
                    allowed.append("bundle_manifest.json")
                continue

            if "/" in rel:
                top = rel.split("/", 1)[0]
                prefix = f"{top}/"
                if prefix not in allowed:
                    allowed.append(prefix)
            else:
                if rel not in allowed:
                    allowed.append(rel)

    if "bundle_manifest.json" not in allowed:
        allowed.insert(0, "bundle_manifest.json")

    return allowed


def repair_manifest(bundle_name, missing_fields, allowed_paths):
    src = os.path.join(FAILED_BUNDLES, bundle_name)
    if not os.path.exists(src):
        return {
            "status": "failed",
            "reason": "bundle_not_found",
            "bundle": bundle_name,
        }

    ensure_dir(INCOMING_BUNDLES)

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_root = os.path.join(tmpdir, "bundle")
        os.makedirs(extract_root, exist_ok=True)

        with zipfile.ZipFile(src, "r") as zf:
            zf.extractall(extract_root)

        manifest_path = os.path.join(extract_root, "bundle_manifest.json")
        manifest = {}

        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
            except Exception:
                manifest = {}

        if not manifest:
            stem = bundle_name[:-4] if bundle_name.endswith(".zip") else bundle_name
            manifest = {
                "bundle_name": stem,
                "bundle_version": "1.0.0",
            }

        if "version" in missing_fields and "version" not in manifest:
            manifest["version"] = "1.0"

        if "install_mode" in missing_fields and "install_mode" not in manifest:
            manifest["install_mode"] = "folder_map"

        if "allowed_paths" in missing_fields and not manifest.get("allowed_paths"):
            manifest["allowed_paths"] = allowed_paths or default_allowed_paths_from_tree(extract_root)

        if not manifest.get("allowed_paths"):
            manifest["allowed_paths"] = allowed_paths or default_allowed_paths_from_tree(extract_root)

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")

        stem = bundle_name[:-4] if bundle_name.endswith(".zip") else bundle_name
        repaired_name = f"{stem}_manifest_fixed.zip"
        repaired_path = os.path.join(INCOMING_BUNDLES, repaired_name)

        with zipfile.ZipFile(repaired_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(extract_root):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, extract_root).replace("\\", "/")
                    zf.write(full, rel)

        return {
            "status": "ok",
            "action": "repair_bundle_manifest",
            "source_bundle": bundle_name,
            "repaired_bundle": repaired_name,
            "repaired_path": repaired_path,
            "manifest_after_repair": manifest,
        }


def reconstruct_bundle_report_match(bundle_name):
    return {
        "status": "noop",
        "action": "reconstruct_bundle_report_match",
        "target": bundle_name,
        "reason": "not_implemented_yet",
    }


def inspect_failed_bundle_family(bundle_name):
    return {
        "status": "noop",
        "action": "inspect_failed_bundle_family",
        "target": bundle_name,
        "reason": "not_implemented_yet",
    }


def mark_bundle_obsolete(bundle_name):
    return {
        "status": "noop",
        "action": "mark_bundle_obsolete",
        "target": bundle_name,
        "reason": "not_implemented_yet",
    }


def maybe_trigger_ingestion():
    workflow_path = os.environ.get("INGESTION_WORKFLOW_PATH", ".github/workflows/ingestion.yml")
    gh_token = os.environ.get("GH_TOKEN", "")

    if not gh_token:
        return {
            "status": "skipped",
            "reason": "GH_TOKEN_missing",
            "workflow": workflow_path,
        }

    try:
        subprocess.run(
            ["gh", "workflow", "run", workflow_path],
            check=True,
            text=True,
            capture_output=True,
        )
        return {
            "status": "ok",
            "workflow": workflow_path,
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "failed",
            "workflow": workflow_path,
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode,
        }


def main():
    next_action_doc = load_json(NEXT_ACTION_PATH, {})
    next_action = next_action_doc.get("next_action", {})

    action = next_action.get("action")
    target = next_action.get("target")
    missing_fields = next_action.get("missing_fields", [])
    allowed_paths = next_action.get("allowed_paths", [])

    result = {
        "generated_at": utc_now(),
        "input": next_action,
    }

    if not action or action == "idle":
        result["execution"] = {
            "status": "noop",
            "reason": "no_action_to_execute",
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    if action == "repair_bundle_manifest":
        execution = repair_manifest(target, missing_fields, allowed_paths)
    elif action == "reconstruct_bundle_report_match":
        execution = reconstruct_bundle_report_match(target)
    elif action == "inspect_failed_bundle_family":
        execution = inspect_failed_bundle_family(target)
    elif action == "mark_bundle_obsolete":
        execution = mark_bundle_obsolete(target)
    else:
        execution = {
            "status": "failed",
            "reason": "unknown_action",
            "action": action,
            "target": target,
        }

    result["execution"] = execution

    if execution.get("status") == "ok" and action == "repair_bundle_manifest":
        result["ingestion_trigger"] = maybe_trigger_ingestion()
    else:
        result["ingestion_trigger"] = {
            "status": "skipped",
            "reason": "no_ingestion_trigger_for_result",
        }

    write_json(OUTPUT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
