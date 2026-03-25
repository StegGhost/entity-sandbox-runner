from pathlib import Path
import json


def _safe_read_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def compute_closure(reconciler_output, state):
    actions = []

    root = Path(state["root"])
    feedback_path = root / "payload" / "feedback" / "failed_bundle_report_correlation.json"

    # --- Existing behavior: failed bundle inspection ---
    failed = reconciler_output.get("counts", {}).get("recent_failed_bundles", 0)
    if failed > 0:
        failed_targets = reconciler_output.get("findings", [])[0].get("evidence", [])[:5]

        actions.append({
            "action": "inspect_failed_bundles",
            "priority": 1,
            "targets": failed_targets,
            "reason": f"{failed} recent failed bundles detected"
        })

    # --- Existing behavior: correlation ---
    actions.append({
        "action": "correlate_failed_bundles_with_ingestion_reports",
        "priority": 2,
        "targets": ["failed_bundles/", "ingestion_reports/"],
        "reason": "Need bundle-to-report closure for diagnosis"
    })

    # --- NEW: repair planning from correlation file ---
    if feedback_path.exists():
        data = _safe_read_json(feedback_path) or {}
        correlations = data.get("correlations", [])

        repair_targets = []

        for item in correlations:
            if item.get("status") != "matched":
                continue

            missing_fields = item.get("missing_fields", [])
            reason = item.get("verification_reason")

            # Only target manifest-related failures for now
            if reason == "manifest_missing_required_fields" or missing_fields:
                repair_targets.append({
                    "bundle": item.get("bundle"),
                    "missing_fields": missing_fields,
                    "reason": reason
                })

        if repair_targets:
            actions.append({
                "action": "repair_bundle_manifests",
                "priority": 3,
                "targets": repair_targets[:5],  # limit scope
                "reason": "Detected manifest schema failures requiring repair"
            })

    return {
        "mode": "active",
        "summary": "Closure engine built ordered action set",
        "actions": actions
    }
