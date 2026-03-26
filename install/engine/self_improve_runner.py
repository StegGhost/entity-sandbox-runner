"""
SELF IMPROVE RUNNER — minimal stable contract implementation

Purpose:
- provide run_self_improve for tests/test_self_improve.py
- keep behavior deterministic
- avoid external dependencies while stabilizing the sandbox baseline
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from install.engine.llm_self_improve import generate_proposal
from install.engine.proposal_to_bundle import proposal_to_bundle


def run_self_improve(
    context: Optional[Dict[str, Any]] = None,
    allowed_paths: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """
    Minimal deterministic self-improve pipeline:

    1. Generate a proposal
    2. Convert proposal to a bundle structure
    3. Return a stable result object
    """
    context = context or {}
    allowed_paths = allowed_paths or []

    proposal = generate_proposal(context)
    bundle = proposal_to_bundle(proposal, allowed_paths=allowed_paths)

    return {
        "status": "ok",
        "context": context,
        "proposal": proposal,
        "bundle": bundle,
    }


def main() -> Dict[str, Any]:
    """
    Simple entry point for direct invocation.
    """
    return run_self_improve({})


if __name__ == "__main__":
    print(main())
