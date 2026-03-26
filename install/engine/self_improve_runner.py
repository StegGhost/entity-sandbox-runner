"""
SELF IMPROVE RUNNER — stable contract implementation

Purpose:
- provide run_self_improve for tests/test_self_improve.py
- accept failure_text keyword argument
- tolerate the first positional arg being either:
  - a snapshot dict
  - a repo root path string like "."
- write a bundle by default so tests can verify bundle existence
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

from install.engine.llm_self_improve import generate_proposal
from install.engine.proposal_to_bundle import proposal_to_bundle


def _coerce_inputs(
    snapshot_or_root: Optional[Any] = None,
    failure_text: str = "",
) -> Tuple[Dict[str, Any], str, str]:
    """
    Normalize inputs into:
    - snapshot dict
    - failure_text string
    - root path string
    """
    if isinstance(snapshot_or_root, dict):
        return snapshot_or_root, failure_text, "."

    if isinstance(snapshot_or_root, str):
        return {}, failure_text, snapshot_or_root

    return {}, failure_text, "."


def run_self_improve(
    snapshot_or_root: Optional[Any] = None,
    failure_text: str = "",
    allowed_paths: Optional[list[str]] = None,
    output_path: str | None = None,
) -> Dict[str, Any]:
    """
    Minimal deterministic self-improve pipeline:

    1. Generate proposal from snapshot + failure_text
    2. Convert proposal into a zip bundle on disk
    3. Return stable result with bundle existence signal
    """
    snapshot, failure_text, root = _coerce_inputs(snapshot_or_root, failure_text)
    allowed_paths = allowed_paths or []

    proposal = generate_proposal(snapshot, failure_text=failure_text)

    bundle_path = output_path
    if not bundle_path:
        bundle_path = os.path.join(root, "incoming_bundles", "auto_bundle.zip")

    bundle_result = proposal_to_bundle(
        proposal,
        allowed_paths=allowed_paths,
        output_path=bundle_path,
    )

    bundle_exists = isinstance(bundle_result, str) and os.path.exists(bundle_result)

    return {
        "status": "ok",
        "snapshot": snapshot,
        "failure_text": failure_text,
        "proposal": proposal,
        "bundle_result": bundle_result,
        "bundle_path": bundle_result,
        "bundle_exists": bundle_exists,
    }


def main() -> Dict[str, Any]:
    return run_self_improve(".")


if __name__ == "__main__":
    print(main())
