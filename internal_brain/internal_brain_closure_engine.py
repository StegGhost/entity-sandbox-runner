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

    findings = reconciler_output.get("findings", [])
    counts = reconciler_output.get("counts", {})

    failed = counts.get("recent_failed_bundles", 0)
    failed_targets = []

    for finding in findings:
        if finding.get("type") == "failed_bundles_present":
            failed_targets = finding.get("evidence", [])[:5]
            break

    if failed > 0:
        actions.append({
            "action": "inspect_failed_bundles",
            "priority": 1,
            "targets": failed_targets,
            "reason": f"{failed} recent failed bundles detected"
        })

    actions.append({
        "action": "correlate_failed_bundles_with_ingestion_reports",
        "priority": 2,
        "targets": [
            "failed_bundles/",
            "ingestion_reports/"
        ],
        "reason": "Need bundle-to-report closure for diagnosis"
    })

    if feedback_path.exists():
        data = _safe_read_json(feedback_path) or {}
        correlations = data.get("correlations", [])

        repair_targets = []

        for item in correlations:
            if item.get("status") != "matched":
                continue

            missing_fields = item.get("missing_fields", [])
            reason = item.get("verification_reason")

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
                "targets": repair_targets[:5],
                "reason": "Detected manifest schema failures requiring repair"
            })

    actions.sort(key=lambda a: a["priority"])

    return {
        "mode": "active",
        "summary": "Closure engine built ordered action set",
        "actions": actions
    }
