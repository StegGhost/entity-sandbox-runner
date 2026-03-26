"""
SELF IMPROVE RUNNER — stable contract implementation

Purpose:
- provide run_self_improve for tests/test_self_improve.py
- accept failure_text keyword argument
- keep behavior deterministic
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from install.engine.llm_self_improve import generate_proposal
from install.engine.proposal_to_bundle import proposal_to_bundle


def run_self_improve(
    snapshot: Optional[Dict[str, Any]] = None,
    failure_text: str = "",
    allowed_paths: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """
    Minimal deterministic self-improve pipeline:

    1. Generate proposal from snapshot + failure_text
    2. Convert proposal into bundle structure
    3. Return stable result
    """
    snapshot = snapshot or {}
    allowed_paths = allowed_paths or []

    proposal = generate_proposal(snapshot, failure_text=failure_text)
    bundle = proposal_to_bundle(proposal, allowed_paths=allowed_paths)

    return {
        "status": "ok",
        "snapshot": snapshot,
        "failure_text": failure_text,
        "proposal": proposal,
        "bundle": bundle,
    }


def main() -> Dict[str, Any]:
    return run_self_improve({})


if __name__ == "__main__":
    print(main())
