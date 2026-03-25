import os
import json
import zipfile
import tempfile
import subprocess
import time
from datetime import datetime

ROOT = os.getcwd()

BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")
FAILED_BUNDLES = os.path.join(ROOT, "failed_bundles")
INCOMING_BUNDLES = os.path.join(ROOT, "incoming_bundles")
LOG_PATH = os.path.join(ROOT, "logs", "ingestion_log.json")

NEXT_ACTION_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")
OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")


def utc_now():
    return datetime.utcnow().isoformat()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


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


def write_json(path, payload):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def load_ingestion_log():
    if not os.path.exists(LOG_PATH):
        return []
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def default_allowed_paths_from_tree(extract_root):
    allowed = []

    for root, _, files in os.walk(extract_root):
        for fname in files:
            full = os.path.join(root, fname)
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


def repair_bundle_manifest(bundle_name, missing_fields, allowed_paths):
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
                for fname in files:
                    full = os.path.join(root, fname)
                    rel = os.path.relpath(full, extract_root).replace("\\", "/")
                    zf.write(full, rel)

        return {
            "status": "ok",
            "executed": True,
            "action": "repair_bundle_manifest",
            "target": bundle_name,
            "repaired_bundle": repaired_name,
            "repaired_path": repaired_path,
            "manifest_after_repair": manifest,
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
        completed = subprocess.run(
            ["gh", "workflow", "run", workflow_path],
            check=True,
            text=True,
            capture_output=True,
        )
        return {
            "status": "ok",
            "workflow": workflow_path,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "failed",
            "workflow": workflow_path,
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode,
        }


def confirm_ingestion(bundle_name, wait_seconds=20):
    start = time.time()
    seen_initial = load_ingestion_log()
    initial_len = len(seen_initial)

    while time.time() - start < wait_seconds:
        log = load_ingestion_log()
        if len(log) > initial_len:
            for entry in reversed(log):
                if entry.get("bundle") == bundle_name:
                    return {
                        "status": "confirmed",
                        "bundle": bundle_name,
                        "ok": entry.get("ok"),
                        "error": entry.get("error"),
                        "ts": entry.get("ts"),
                    }
        time.sleep(2)

    return {
        "status": "pending_ingestion_confirmation",
        "bundle": bundle_name,
        "reason": "no matching ingestion log entry observed within wait window",
    }


def main():
    ensure_dir(BRAIN_REPORTS)

    next_action_doc = load_json(NEXT_ACTION_PATH, {})
    next_action = next_action_doc.get("next_action", {})

    action = next_action.get("action")
    target = next_action.get("target")
    missing_fields = next_action.get("missing_fields", [])
    allowed_paths = next_action.get("allowed_paths", [])

    result = {
        "generated_at": utc_now(),
        "input_document": next_action_doc,
        "resolved_next_action": next_action,
    }

    if not action or action == "idle":
        result["execution"] = {
            "status": "noop",
            "executed": False,
            "reason": "no_action_to_execute",
            "action": action,
            "target": target,
        }
        result["ingestion_trigger"] = {
            "status": "skipped",
            "reason": "no_ingestion_trigger_for_result",
        }
        result["ingestion_confirmation"] = {
            "status": "skipped",
            "reason": "no_ingestion_trigger_for_result",
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    if action == "repair_bundle_manifest":
        execution = repair_bundle_manifest(target, missing_fields, allowed_paths)
    else:
        execution = {
            "status": "failed",
            "executed": False,
            "reason": "unknown_or_unsupported_action",
            "action": action,
            "target": target,
        }

    result["execution"] = execution

    if execution.get("status") == "ok" and action == "repair_bundle_manifest":
        trigger = maybe_trigger_ingestion()
        result["ingestion_trigger"] = trigger
        if trigger.get("status") == "ok":
            result["ingestion_confirmation"] = confirm_ingestion(execution.get("repaired_bundle"))
        else:
            result["ingestion_confirmation"] = {
                "status": "skipped",
                "reason": "ingestion_not_triggered",
            }
    else:
        result["ingestion_trigger"] = {
            "status": "skipped",
            "reason": "no_ingestion_trigger_for_result",
        }
        result["ingestion_confirmation"] = {
            "status": "skipped",
            "reason": "no_ingestion_trigger_for_result",
        }

    write_json(OUTPUT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
