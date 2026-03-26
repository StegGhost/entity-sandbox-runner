"""
SELF IMPROVE RUNNER — stable contract implementation

Purpose:
- provide run_self_improve for tests/test_self_improve.py
- accept failure_text keyword argument
- tolerate failure_text passed as first positional arg
- optionally write generated bundle to output_path
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from install.engine.llm_self_improve import generate_proposal
from install.engine.proposal_to_bundle import proposal_to_bundle


def _coerce_inputs(
    snapshot: Optional[Dict[str, Any]] = None,
    failure_text: str = "",
) -> tuple[Dict[str, Any], str]:
    if isinstance(snapshot, str):
        return {}, snapshot

    if snapshot is None:
        return {}, failure_text

    if not isinstance(snapshot, dict):
        return {}, failure_text

    return snapshot, failure_text


def run_self_improve(
    snapshot: Optional[Dict[str, Any]] = None,
    failure_text: str = "",
    allowed_paths: Optional[list[str]] = None,
    output_path: str | None = None,
) -> Dict[str, Any]:
    """
    Minimal deterministic self-improve pipeline:

    1. Generate proposal from snapshot + failure_text
    2. Convert proposal into bundle structure or zip output
    3. Return stable result
    """
    snapshot, failure_text = _coerce_inputs(snapshot, failure_text)
    allowed_paths = allowed_paths or []

    proposal = generate_proposal(snapshot, failure_text=failure_text)
    bundle_result = proposal_to_bundle(
        proposal,
        allowed_paths=allowed_paths,
        output_path=output_path,
    )

    return {
        "status": "ok",
        "snapshot": snapshot,
        "failure_text": failure_text,
        "proposal": proposal,
        "bundle_result": bundle_result,
    }


def main() -> Dict[str, Any]:
    return run_self_improve({})


if __name__ == "__main__":
    print(main())
