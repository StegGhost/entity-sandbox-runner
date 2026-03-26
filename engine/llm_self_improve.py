"""
LLM SELF IMPROVE ENGINE — stable contract implementation

Purpose:
- provide deterministic proposal generation
- satisfy self_improve + failure_feedback tests
- accept failure_text keyword argument
- tolerate snapshot being missing or incorrectly passed as a string
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def _coerce_snapshot_and_failure_text(
    snapshot: Optional[Dict[str, Any]] = None,
    failure_text: str = "",
) -> tuple[Dict[str, Any], str]:
    """
    Some callers may accidentally pass failure_text as the first positional arg.
    This normalizes that into:
      snapshot -> dict
      failure_text -> str
    """
    if isinstance(snapshot, str):
        return {}, snapshot

    if snapshot is None:
        return {}, failure_text

    if not isinstance(snapshot, dict):
        return {}, failure_text

    return snapshot, failure_text


def classify_gaps(
    snapshot: Optional[Dict[str, Any]] = None,
    failure_text: str = "",
) -> List[str]:
    snapshot, failure_text = _coerce_snapshot_and_failure_text(snapshot, failure_text)

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
    - failure_text accidentally passed as first positional arg
    """
    snapshot, failure_text = _coerce_snapshot_and_failure_text(snapshot, failure_text)
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
