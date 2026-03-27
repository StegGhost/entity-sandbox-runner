import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import json
import re
import subprocess
from datetime import datetime

ROOT = os.getcwd()
BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")
INTERNAL_BRAIN_REPORT = os.path.join(ROOT, "internal_brain", "brain_report.json")

RECEIPT_RECONCILED_STATE = os.path.join(BRAIN_REPORTS, "receipt_reconciled_state.json")
BUNDLE_INVENTORY = os.path.join(BRAIN_REPORTS, "bundle_inventory.json")
FAILED_CORRELATION = os.path.join(BRAIN_REPORTS, "failed_bundle_report_correlation.json")
EXECUTION_RESULT = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")
RECONCILED_STATE = os.path.join(BRAIN_REPORTS, "reconciled_state.json")
OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")


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
    family_members = {}

    inv = inventory.get("inventory", {})

    for state_name, files in inv.items():
        for fname in files:
            bundle_to_state[fname] = state_name
            fk = family_key(fname)
            family_members.setdefault(fk, []).append(fname)

    for fk, members in family_members.items():
        family_members[fk] = sorted(
            members,
            key=lambda x: (
                extract_version(x) if extract_version(x) is not None else 10**9,
                x,
            ),
        )

    return bundle_to_state, family_members


def build_correlation_map(correlations):
    corr_by_bundle = {}
    for c in correlations:
        bundle_name = c.get("bundle_name")
        if bundle_name:
            corr_by_bundle[bundle_name] = c
    return corr_by_bundle


def installed_family_set(bundle_to_state, family_members):
    families = set()
    for fk, members in family_members.items():
        for member in members:
            if bundle_to_state.get(member) == "installed":
                families.add(fk)
                break
    return families


def build_classification(bundle_to_state, family_members, correlations):
    manifest_repairable = []
    missing_report = []
    unresolved_failed = []
    obsolete_candidates = []

    installed_families = installed_family_set(bundle_to_state, family_members)
    corr_by_bundle = build_correlation_map(correlations)

    failed_names = sorted(
        [bundle for bundle, state in bundle_to_state.items() if state == "failed"],
        key=lambda x: (
            family_key(x),
            extract_version(x) if extract_version(x) is not None else 10**9,
            x,
        ),
    )

    for bundle_name in failed_names:
        corr = corr_by_bundle.get(bundle_name)
        fk = family_key(bundle_name)

        if fk in installed_families:
            obsolete_candidates.append(
                {
                    "bundle": bundle_name,
                    "family": fk,
                    "reason": "same family has an installed member",
                }
            )
            continue

        if not corr:
            unresolved_failed.append(
                {
                    "bundle": bundle_name,
                    "family": fk,
                    "reason": "no correlation entry",
                }
            )
            continue

        if corr.get("status") == "no_report_found":
            missing_report.append(
                {
                    "bundle": bundle_name,
                    "family": fk,
                    "reason": "no matched ingestion report",
                }
            )
            continue

        missing_fields = corr.get("missing_fields", [])
        verification_reason = corr.get("verification_reason")

        if verification_reason == "manifest_missing_required_fields" or missing_fields:
            manifest_repairable.append(
                {
                    "bundle": bundle_name,
                    "family": fk,
                    "reason": verification_reason or "manifest_missing_required_fields",
                    "missing_fields": missing_fields,
                    "allowed_paths": corr.get("allowed_paths", []),
                }
            )
        else:
            unresolved_failed.append(
                {
                    "bundle": bundle_name,
                    "family": fk,
                    "reason": "matched report but no supported repair class yet",
                }
            )

    manifest_repairable = sorted(
        manifest_repairable,
        key=lambda x: (
            x["family"],
            extract_version(x["bundle"]) if extract_version(x["bundle"]) is not None else 10**9,
            x["bundle"],
        ),
    )
    missing_report = sorted(
        missing_report,
        key=lambda x: (
            x["family"],
            extract_version(x["bundle"]) if extract_version(x["bundle"]) is not None else 10**9,
            x["bundle"],
        ),
    )
    unresolved_failed = sorted(
        unresolved_failed,
        key=lambda x: (
            x["family"],
            extract_version(x["bundle"]) if extract_version(x["bundle"]) is not None else 10**9,
            x["bundle"],
        ),
    )
    obsolete_candidates = sorted(
        obsolete_candidates,
        key=lambda x: (
            x["family"],
            extract_version(x["bundle"]) if extract_version(x["bundle"]) is not None else 10**9,
            x["bundle"],
        ),
    )

    return manifest_repairable, missing_report, unresolved_failed, obsolete_candidates


def get_active_family(last_execution_doc):
    execution = last_execution_doc.get("execution", {})
    if execution.get("status") != "ok":
        return None

    action = execution.get("action")
    if action != "repair_bundle_manifest":
        return None

    repaired_target = execution.get("target")
    if not repaired_target:
        return None

    return family_key(repaired_target)


def get_last_executed_bundle(last_execution_doc):
    execution = last_execution_doc.get("execution", {})
    if execution.get("status") != "ok":
        return None
    return execution.get("target")


def get_last_execution_action(last_execution_doc):
    execution = last_execution_doc.get("execution", {})
    if execution.get("status") != "ok":
        return None
    return execution.get("action")


def get_reconcile_review(reconciled_doc):
    if not isinstance(reconciled_doc, dict):
        return {}
    review = reconciled_doc.get("review", {})
    return review if isinstance(review, dict) else {}


def first_matching_family(items, family, skip_bundle=None):
    for item in items:
        if item.get("family") == family and item.get("bundle") != skip_bundle:
            return item
    return None


def choose_repair_escalation(reconciled_doc, last_execution_doc):
    review = get_reconcile_review(reconciled_doc)
    last_action = get_last_execution_action(last_execution_doc)
    last_bundle = get_last_executed_bundle(last_execution_doc)

    review_state = review.get("state")
    review_family = review.get("family")
    review_bundle = review.get("bundle")
    review_reason = review.get("reason")

    if review_state != "failed":
        return None

    if last_action != "inspect_failed_bundle_family":
        return None

    bundle = review_bundle or last_bundle
    family = review_family or family_key(bundle) if bundle else None

    if not bundle or not family:
        return None

    return {
        "ts": utc_now(),
        "status": "ok",
        "selection_mode": "repair_escalation",
        "active_family": family,
        "action": "propose_repair_for_bundle_family",
        "target": bundle,
        "family": family,
        "priority": "high",
        "reason": review_reason or "inspection_completed_but_failure_persists",
        "source": "repair_escalation",
    }


def choose_next_action(
    manifest_repairable,
    missing_report,
    unresolved_failed,
    obsolete_candidates,
    active_family,
    last_bundle,
):
    if active_family:
        target = first_matching_family(manifest_repairable, active_family, skip_bundle=last_bundle)
        if target:
            return {
                "ts": utc_now(),
                "status": "ok",
                "selection_mode": "active_family_continuation",
                "active_family": active_family,
                "action": "repair_bundle_manifest",
                "target": target["bundle"],
                "family": target["family"],
                "priority": "high",
                "reason": target["reason"],
                "missing_fields": target.get("missing_fields", []),
                "allowed_paths": target.get("allowed_paths", []),
            }

        target = first_matching_family(missing_report, active_family, skip_bundle=last_bundle)
        if target:
            return {
                "ts": utc_now(),
                "status": "ok",
                "selection_mode": "active_family_continuation",
                "active_family": active_family,
                "action": "reconstruct_bundle_report_match",
                "target": target["bundle"],
                "family": target["family"],
                "priority": "high",
                "reason": target["reason"],
            }

        target = first_matching_family(unresolved_failed, active_family, skip_bundle=last_bundle)
        if target:
            return {
                "ts": utc_now(),
                "status": "ok",
                "selection_mode": "active_family_continuation",
                "active_family": active_family,
                "action": "inspect_failed_bundle_family",
                "target": target["bundle"],
                "family": target["family"],
                "priority": "medium",
                "reason": target["reason"],
            }

    if manifest_repairable:
        target = manifest_repairable[0]
        return {
            "ts": utc_now(),
            "status": "ok",
            "selection_mode": "global_scan",
            "active_family": active_family,
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
            "selection_mode": "global_scan",
            "active_family": active_family,
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
            "selection_mode": "global_scan",
            "active_family": active_family,
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
            "selection_mode": "global_scan",
            "active_family": active_family,
            "action": "mark_bundle_obsolete",
            "target": target["bundle"],
            "family": target["family"],
            "priority": "low",
            "reason": target["reason"],
        }

    return {
        "ts": utc_now(),
        "status": "ok",
        "selection_mode": "idle",
        "active_family": active_family,
        "action": "idle",
        "target": None,
        "family": None,
        "priority": "low",
        "reason": "no admissible next action found",
    }


def run_internal_brain():
    runner = os.path.join(ROOT, "internal_brain", "brain_runner.py")
    if not os.path.exists(runner):
        return {"status": "missing", "reason": "brain_runner_not_found"}

    try:
        completed = subprocess.run(
            [sys.executable, runner],
            check=True,
            text=True,
            capture_output=True,
        )
        return {
            "status": "ok",
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "failed",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode,
        }


def map_internal_brain_action(report):
    closure = report.get("closure_output", {})
    actions = closure.get("actions", [])

    if not actions:
        return None

    first = actions[0]
    action_name = first.get("action")
    reason = first.get("reason", "internal_brain_action")
    targets = first.get("targets", [])

    if action_name == "repair_bundle_manifests" and targets:
        target = targets[0]
        if isinstance(target, dict):
            bundle = target.get("bundle")
            if bundle:
                return {
                    "ts": utc_now(),
                    "status": "ok",
                    "selection_mode": "internal_brain_closure",
                    "active_family": family_key(bundle),
                    "action": "repair_bundle_manifest",
                    "target": bundle,
                    "family": family_key(bundle),
                    "priority": first.get("priority", "high"),
                    "reason": target.get("reason", reason),
                    "missing_fields": target.get("missing_fields", []),
                    "allowed_paths": target.get("allowed_paths", []),
                    "source": "internal_brain",
                }

    if action_name == "inspect_failed_bundles" and targets:
        bundle = targets[0]
        if isinstance(bundle, str):
            return {
                "ts": utc_now(),
                "status": "ok",
                "selection_mode": "internal_brain_closure",
                "active_family": family_key(bundle),
                "action": "inspect_failed_bundle_family",
                "target": bundle,
                "family": family_key(bundle),
                "priority": first.get("priority", "medium"),
                "reason": reason,
                "source": "internal_brain",
            }

    if action_name == "correlate_failed_bundles_with_ingestion_reports":
        return {
            "ts": utc_now(),
            "status": "ok",
            "selection_mode": "internal_brain_closure",
            "active_family": None,
            "action": "reconstruct_bundle_report_match",
            "target": None,
            "family": None,
            "priority": first.get("priority", "high"),
            "reason": reason,
            "source": "internal_brain",
        }

    return None


def main():
    ensure_dir(BRAIN_REPORTS)

    internal_brain_run = run_internal_brain()
    internal_brain_report = load_json(INTERNAL_BRAIN_REPORT, {})
    mapped_action = None
    if internal_brain_run.get("status") == "ok" and internal_brain_report:
        mapped_action = map_internal_brain_action(internal_brain_report)

    _ = load_json(RECEIPT_RECONCILED_STATE, {})
    inventory = load_json(BUNDLE_INVENTORY, {"inventory": {}})
    correlation = load_json(FAILED_CORRELATION, {"correlations": []})
    last_execution = load_json(EXECUTION_RESULT, {})
    reconciled_state = load_json(RECONCILED_STATE, {})

    bundle_to_state, family_members = build_inventory_maps(inventory)
    correlations = correlation.get("correlations", [])

    manifest_repairable, missing_report, unresolved_failed, obsolete_candidates = build_classification(
        bundle_to_state,
        family_members,
        correlations,
    )

    active_family = get_active_family(last_execution)
    last_bundle = get_last_executed_bundle(last_execution)

    repair_escalation = choose_repair_escalation(reconciled_state, last_execution)

    next_action = repair_escalation or mapped_action or choose_next_action(
        manifest_repairable,
        missing_report,
        unresolved_failed,
        obsolete_candidates,
        active_family,
        last_bundle,
    )

    output = {
        "generated_at": utc_now(),
        "summary": {
            "manifest_repairable_count": len(manifest_repairable),
            "missing_report_count": len(missing_report),
            "unresolved_failed_count": len(unresolved_failed),
            "obsolete_candidate_count": len(obsolete_candidates),
            "total_failed_seen": len([b for b, state in bundle_to_state.items() if state == "failed"]),
            "active_family": active_family,
            "last_executed_bundle": last_bundle,
            "internal_brain_status": internal_brain_run.get("status"),
            "repair_escalation_active": repair_escalation is not None,
        },
        "next_action": next_action,
        "candidates": {
            "manifest_repairable": manifest_repairable[:50],
            "missing_report": missing_report[:50],
            "unresolved_failed": unresolved_failed[:50],
            "obsolete_candidates": obsolete_candidates[:50],
        },
        "internal_brain": {
            "run": internal_brain_run,
            "report_path": INTERNAL_BRAIN_REPORT,
            "mapped_action": mapped_action,
        },
        "repair_escalation": repair_escalation,
        "reconciled_review": get_reconcile_review(reconciled_state),
    }

    write_json(OUTPUT_PATH, output)

    print(
        json.dumps(
            {
                "status": "ok",
                "output": OUTPUT_PATH,
                "next_action": next_action,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
