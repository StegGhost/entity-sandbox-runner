from typing import Any, Dict, List

def compute_closure(reconciled_output: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    actions: List[Dict[str, Any]] = []

    for finding in reconciled_output.get("findings", []):
        ftype = finding.get("type")
        if ftype == "failed_bundles_present":
            actions.append({
                "action": "inspect_failed_bundles",
                "priority": 1,
                "targets": finding.get("evidence", []),
                "reason": finding.get("detail")
            })
            actions.append({
                "action": "correlate_failed_bundles_with_ingestion_reports",
                "priority": 2,
                "targets": ["failed_bundles/", "ingestion_reports/"],
                "reason": "Need bundle-to-report closure for diagnosis"
            })
        elif ftype == "missing_ingestion_reports":
            actions.append({
                "action": "inspect_ingestion_pipeline_reporting",
                "priority": 1,
                "targets": ["ingestion_reports/"],
                "reason": finding.get("detail")
            })

    if not actions:
        actions.append({
            "action": "no_action_required",
            "priority": 99,
            "targets": [],
            "reason": "No actionable findings"
        })

    actions.sort(key=lambda a: a["priority"])

    return {
        "mode": "ingested_module",
        "summary": "Closure engine built ordered action set",
        "actions": actions
    }
