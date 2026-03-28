import os
import json
from datetime import datetime


INVENTORY_PATH = "brain_reports/bundle_inventory.json"
FAILED_REPORT_PATH = "brain_reports/failed_bundle_report_correlation.json"
OUTPUT_PATH = "brain_reports/repair_bundle_engine_result.json"


def now_ts():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def extract_bundle_name(entry):
    # Flexible extraction across possible formats
    for key in ["bundle", "bundle_name", "file", "path", "name"]:
        if key in entry and entry[key]:
            return os.path.basename(entry[key])
    return None


def resolve_family(bundle_name, manifest=None):
    # 1. manifest-defined family (future-proof)
    if manifest and manifest.get("family"):
        return manifest["family"]

    # 2. standard naming patterns
    if "_bundle" in bundle_name:
        return bundle_name.split("_bundle")[0]

    if "_" in bundle_name:
        return bundle_name.split("_")[0]

    return "unknown"


def find_latest_bundle_for_family(family, inventory):
    if not inventory:
        return None

    candidates = []

    for item in inventory.get("bundles", []):
        name = item.get("name") or item.get("file")
        if not name:
            continue

        if name.startswith(family):
            candidates.append(name)

    if not candidates:
        return None

    # sort by version-like suffix (best effort)
    candidates.sort(reverse=True)
    return candidates[0]


def build_result(status, action=None, family=None, target=None, reason=None):
    return {
        "status": status,
        "ts": now_ts(),
        "action": action,
        "family": family,
        "target": target,
        "resolved_path": None,
        "worker_result": None,
        "reintegrate_result": None,
        "reason": reason,
        "output_report": OUTPUT_PATH,
    }


def main():
    failed_report = load_json(FAILED_REPORT_PATH)
    inventory = load_json(INVENTORY_PATH)

    if not failed_report:
        result = build_result(
            status="noop",
            reason="no_failed_report"
        )
        write_output(result)
        return result

    failures = failed_report.get("failures") or []

    if not failures:
        result = build_result(
            status="noop",
            reason="no_failures_detected"
        )
        write_output(result)
        return result

    # Take first actionable failure (deterministic for now)
    entry = failures[0]

    bundle_name = extract_bundle_name(entry)

    if not bundle_name:
        raise Exception("repair_engine: could not extract bundle name")

    family = resolve_family(bundle_name)

    if family == "unknown":
        raise Exception(f"repair_engine: family resolution failed for {bundle_name}")

    target = find_latest_bundle_for_family(family, inventory)

    # fallback: self-target (critical for convergence)
    if not target:
        target = bundle_name

    if not target:
        raise Exception("repair_engine: target resolution failed (empty)")

    result = build_result(
        status="ok",
        action="propose_repair_for_bundle_family",
        family=family,
        target=target,
        reason="resolved"
    )

    write_output(result)
    return result


def write_output(data):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    output = main()
    print(json.dumps({
        "status": output["status"],
        "output": OUTPUT_PATH,
        "result": output
    }, indent=2))
