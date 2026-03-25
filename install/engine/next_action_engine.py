import os
import json
import re
from datetime import datetime

ROOT = os.getcwd()

BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")

RECEIPT_RECONCILED_STATE = os.path.join(BRAIN_REPORTS, "receipt_reconciled_state.json")
BUNDLE_INVENTORY = os.path.join(BRAIN_REPORTS, "bundle_inventory.json")
FAILED_CORRELATION = os.path.join(BRAIN_REPORTS, "failed_bundle_report_correlation.json")

OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")


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


def family_key(name: str) -> str:
    name = os.path.basename(name)
    if name.endswith(".zip"):
        name = name[:-4]

    name = re.sub(r"_manifest_fixed$", "", name)
    name = re.sub(r"_fixed$", "", name)
    name = re.sub(r"_bundle$", "", name)
    name = re.sub(r"_v\d+$", "", name)

    return name


def extract_version(name: str):
    m = re.search(r"_v(\d+)", name)
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None


def build_inventory_maps(inventory):
    bundle_to_state = {}
    bundle_to_location = {}
    family_members = {}

    inv = inventory.get("inventory", {})

    for state_name, files in inv.items():
        for fname in files:
            bundle_to_state[fname] = state_name
            bundle_to_location[fname] = state_name
            fk = family_key(fname)
            family_members.setdefault(fk, []).append(fname)

    for fk, members in family_members.items():
        family_members[fk] = sorted(
            members,
            key=lambda x: (
                extract_version(x) if extract_version(x) is not None else -1,
                x
            )
        )

    return bundle_to_state, bundle_to_location, family_members


def classify_candidates(correlations, bundle_to_state, family_members):
    manifest_repairable = []
    missing_report = []
    unresolved_failed = []
    obsolete_candidates = []

    installed_families = set()

    for fk, members in family_members.items():
        for m in members:
            if bundle_to_state.get(m) == "installed":
                installed_families.add(fk)
                break

    corr_by_bundle = {}
    for c in correlations:
        corr_by_bundle[c.get("bundle_name")] = c

    failed_names = [b for b, state in bundle_to_state.items() if state == "failed"]

    for bundle_name in failed_names:
        corr = corr_by_bundle.get(bundle_name)
        fk = family_key(bundle_name)

        if fk in installed_families:
            obsolete_candidates.append({
                "bundle": bundle_name,
                "family": fk,
                "reason": "same family has an installed member"
            })
            continue

        if not corr:
            unresolved_failed.append({
                "bundle": bundle_name,
                "family": fk,
                "reason": "no correlation entry"
            })
            continue

        if corr.get("status") == "no_report_found":
            missing_report.append({
                "bundle": bundle_name,
                "family": fk,
                "reason": "no matched ingestion report"
            })
            continue

        missing_fields = corr.get("missing_fields", [])
        verification_reason = corr.get("verification_reason")

        if verification_reason == "manifest_missing_required_fields" or missing_fields:
            manifest_repairable.append({
                "bundle": bundle_name,
                "family": fk,
                "reason": verification_reason or "manifest_missing_required_fields",
                "missing_fields": missing_fields,
                "allowed_paths": corr.get("allowed_paths", []),
            })
        else:
            unresolved_failed.append({
                "bundle": bundle_name,
                "family": fk,
                "reason": "matched report but no supported repair class yet"
            })

    manifest_repairable = sorted(
        manifest_repairable,
        key=lambda x: (
            extract_version(x["bundle"]) if extract_version(x["bundle"]) is not None else 10**9,
            x["bundle"]
        )
    )

    missing_report = sorted(
        missing_report,
        key=lambda x: (
            extract_version(x["bundle"]) if extract_version(x["bundle"]) is not None else 10**9,
            x["bundle"]
        )
    )

    unresolved_failed = sorted(
        unresolved_failed,
        key=lambda x: (
            extract_version(x["bundle"]) if extract_version(x["bundle"]) is not None else 10**9,
            x["bundle"]
        )
    )

    obsolete_candidates = sorted(
        obsolete_candidates,
        key=lambda x: (
            extract_version(x["bundle"]) if extract_version(x["bundle"]) is not None else 10**9,
            x["bundle"]
        )
    )

    return manifest_repairable, missing_report, unresolved_failed, obsolete_candidates


def choose_next_action(manifest_repairable, missing_report, unresolved_failed, obsolete_candidates):
    if manifest_repairable:
        target = manifest_repairable[0]
        return {
            "ts": utc_now(),
            "status": "ok",
            "action": "repair_bundle_manifest",
            "target": target["bundle"],
            "family": target["family"],
            "priority": "high",
            "reason": target["reason"],
            "missing_fields": target.get("missing_fields", []),
            "allowed_paths": target.get("allowed_paths", []),
        }

    if missing_report:
        target = missing_report[0]
        return {
            "ts": utc_now(),
            "status": "ok",
            "action": "reconstruct_bundle_report_match",
            "target": target["bundle"],
            "family": target["family"],
            "priority": "high",
            "reason": target["reason"],
        }

    if unresolved_failed:
        target = unresolved_failed[0]
        return {
            "ts": utc_now(),
            "status": "ok",
            "action": "inspect_failed_bundle_family",
            "target": target["bundle"],
            "family": target["family"],
            "priority": "medium",
            "reason": target["reason"],
        }

    if obsolete_candidates:
        target = obsolete_candidates[0]
        return {
            "ts": utc_now(),
            "status": "ok",
            "action": "mark_bundle_obsolete",
            "target": target["bundle"],
            "family": target["family"],
            "priority": "low",
            "reason": target["reason"],
        }

    return {
        "ts": utc_now(),
        "status": "ok",
        "action": "idle",
        "target": None,
        "family": None,
        "priority": "low",
        "reason": "no admissible next action found",
    }


def main():
    _ = load_json(RECEIPT_RECONCILED_STATE, {})
    inventory = load_json(BUNDLE_INVENTORY, {"inventory": {}})
    correlation = load_json(FAILED_CORRELATION, {"correlations": []})

    bundle_to_state, bundle_to_location, family_members = build_inventory_maps(inventory)
    correlations = correlation.get("correlations", [])

    manifest_repairable, missing_report, unresolved_failed, obsolete_candidates = classify_candidates(
        correlations,
        bundle_to_state,
        family_members,
    )

    next_action = choose_next_action(
        manifest_repairable,
        missing_report,
        unresolved_failed,
        obsolete_candidates,
    )

    output = {
        "generated_at": utc_now(),
        "summary": {
            "manifest_repairable_count": len(manifest_repairable),
            "missing_report_count": len(missing_report),
            "unresolved_failed_count": len(unresolved_failed),
            "obsolete_candidate_count": len(obsolete_candidates),
            "total_failed_seen": len([b for b, state in bundle_to_state.items() if state == "failed"]),
        },
        "next_action": next_action,
        "candidates": {
            "manifest_repairable": manifest_repairable[:20],
            "missing_report": missing_report[:20],
            "unresolved_failed": unresolved_failed[:20],
            "obsolete_candidates": obsolete_candidates[:20],
        }
    }

    os.makedirs(BRAIN_REPORTS, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(json.dumps({
        "status": "ok",
        "output": OUTPUT_PATH,
        "next_action": next_action,
    }, indent=2))


if __name__ == "__main__":
    main()
