"""
LLM SELF IMPROVE ENGINE — stable contract implementation

Purpose:
- provide deterministic proposal generation
- satisfy self_improve + failure_feedback tests
- accept failure_text keyword argument
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def classify_gaps(snapshot: Optional[Dict[str, Any]] = None, failure_text: str = "") -> List[str]:
    snapshot = snapshot or {}
    gaps: List[str] = []

    if snapshot.get("test_count", 0) < 3:
        gaps.append("low_test_coverage")

    if not snapshot.get("has_cge", True):
        gaps.append("missing_cge_root")

    if "ModuleNotFoundError" in failure_text:
        gaps.append("missing_module")

    if "ImportError" in failure_text:
        gaps.append("import_failure")

    if "KeyError" in failure_text:
        gaps.append("contract_mismatch")

    if "AssertionError" in failure_text:
        gaps.append("behavior_failure")

    return list(dict.fromkeys(gaps))


def generate_proposal(
    snapshot: Optional[Dict[str, Any]] = None,
    failure_text: str = "",
) -> Dict[str, Any]:
    """
    Deterministic proposal generator.

    Accepts:
    - snapshot
    - failure_text keyword argument
    """
    snapshot = snapshot or {}
    gaps = classify_gaps(snapshot, failure_text=failure_text)

    return {
        "proposal_id": "auto-proposal-001",
        "proposal_name": "priority_fix",
        "action": "noop",
        "reason": "baseline proposal for system stabilization",
        "confidence": 0.5,
        "gaps": gaps,
        "selected_gap": gaps[0] if gaps else None,
        "files_to_create": [],
        "metadata": {
            "source": "llm_self_improve_stub",
            "failure_text_present": bool(failure_text),
        },
    }
