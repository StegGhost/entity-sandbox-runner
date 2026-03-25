from typing import Any, Dict, List

def reconcile(explorer_output: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    counts = explorer_output.get("counts", {})
    obs = explorer_output.get("observations", {})
    findings: List[Dict[str, Any]] = []

    failed = counts.get("recent_failed_bundles", 0)
    reports = counts.get("recent_ingestion_reports", 0)
    installed = counts.get("recent_installed_bundles", 0)

    if failed > 0:
        findings.append({
            "severity": "high",
            "type": "failed_bundles_present",
            "detail": f"{failed} recent failed bundles detected",
            "evidence": obs.get("recent_failed_bundles", [])[:5]
        })

    if reports == 0:
        findings.append({
            "severity": "high",
            "type": "missing_ingestion_reports",
            "detail": "No recent ingestion reports detected",
            "evidence": []
        })

    if installed > 0:
        findings.append({
            "severity": "low",
            "type": "installed_bundles_present",
            "detail": f"{installed} recent installed bundles detected",
            "evidence": obs.get("recent_installed_bundles", [])[:5]
        })

    healthy = not any(f["severity"] == "high" for f in findings)

    return {
        "mode": "ingested_module",
        "summary": "Reconciler converted observations into prioritized findings",
        "healthy": healthy,
        "findings": findings,
        "counts": counts
    }
