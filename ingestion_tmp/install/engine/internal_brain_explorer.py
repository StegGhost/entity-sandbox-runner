from pathlib import Path
from typing import Any, Dict, List

def _recent_files(root: Path, rel: str, patterns: List[str], limit: int = 20) -> List[str]:
    d = root / rel
    if not d.exists():
        return []
    files = []
    for pattern in patterns:
        files.extend([p for p in d.glob(pattern) if p.is_file()])
    files = sorted(set(files), key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p.relative_to(root)) for p in files[:limit]]

def explore(state: Dict[str, Any]) -> Dict[str, Any]:
    root = Path(state["root"])
    observations = {
        "recent_failed_bundles": _recent_files(root, "failed_bundles", ["*.zip", "*.json"]),
        "recent_installed_bundles": _recent_files(root, "installed_bundles", ["*.zip", "*.json"]),
        "recent_ingestion_reports": _recent_files(root, "ingestion_reports", ["*.json", "*.md", "*.log"]),
        "recent_feedback": _recent_files(root, "payload/feedback", ["*.json", "*.md"]),
        "recent_receipts": _recent_files(root, "receipts", ["*.json", "**/*.json"]),
    }
    counts = {k: len(v) for k, v in observations.items()}
    return {
        "mode": "ingested_module",
        "summary": "Explorer collected current repo signals",
        "counts": counts,
        "observations": observations
    }
