"""
STATE CLASSIFIER — minimal deterministic mutation classifier

Purpose:
- interpret pre/post snapshot differences
- convert raw diff signal into structured categories
- remain fully deterministic (no LLM)
"""

from __future__ import annotations

from typing import Dict, Any


def classify_state_change(pre: Dict[str, Any], post: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(pre, dict) or not isinstance(post, dict):
        return {
            "type": "invalid_snapshot",
            "severity": "critical",
            "action": "halt",
        }

    changes = []

    if pre.get("repo_hash") != post.get("repo_hash"):
        changes.append("repo_modified")

    if pre.get("incoming_bundle_count") != post.get("incoming_bundle_count"):
        changes.append("bundle_queue_changed")

    if pre.get("runtime_report_count") != post.get("runtime_report_count"):
        changes.append("runtime_activity_changed")

    if not changes:
        return {
            "type": "no_change",
            "severity": "none",
            "action": "noop",
        }

    if "repo_modified" in changes:
        return {
            "type": "repo_mutation",
            "severity": "high",
            "action": "inspect_changes",
            "signals": changes,
        }

    return {
        "type": "system_activity",
        "severity": "low",
        "action": "observe",
        "signals": changes,
    }
