import json
import os
import hashlib
from typing import Dict, Any, List


# -------------------------
# FAILURE CLASSIFIER
# -------------------------

def classify_failure(failure_text: str) -> Dict[str, Any]:
    if "multiple children found (fork detected)" in failure_text:
        return {
            "type": "receipt_chain_fork",
            "severity": "high",
        }

    if "cycle detected in receipt chain" in failure_text:
        return {
            "type": "receipt_chain_cycle",
            "severity": "high",
        }

    return {
        "type": "unknown",
        "severity": "low",
    }


# -------------------------
# REPAIR STRATEGIES
# -------------------------

def repair_fork_strategy_linearize() -> Dict[str, Any]:
    return {
        "name": "linearize_chain",
        "description": "Select one child per node and discard others",
        "code": """
def resolve_fork(children):
    return [children[0]]
"""
    }


def repair_fork_strategy_quarantine() -> Dict[str, Any]:
    return {
        "name": "quarantine_fork",
        "description": "Move conflicting receipts to quarantine",
        "code": """
def resolve_fork(children):
    return [c for c in children if c.get("valid")]
"""
    }


def repair_fork_strategy_score() -> Dict[str, Any]:
    return {
        "name": "score_based_selection",
        "description": "Select highest trust score",
        "code": """
def resolve_fork(children):
    return sorted(children, key=lambda x: x.get("authority", {}).get("trust_score", 0), reverse=True)[:1]
"""
    }


# -------------------------
# STRATEGY GENERATOR
# -------------------------

def generate_strategies(failure_type: str) -> List[Dict[str, Any]]:
    if failure_type == "receipt_chain_fork":
        return [
            repair_fork_strategy_linearize(),
            repair_fork_strategy_quarantine(),
            repair_fork_strategy_score(),
        ]

    return []


# -------------------------
# STRATEGY SELECTOR
# -------------------------

def select_best_strategy(strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Simple heuristic for now: prefer score-based
    for s in strategies:
        if s["name"] == "score_based_selection":
            return s
    return strategies[0] if strategies else {}


# -------------------------
# BUNDLE BUILDER
# -------------------------

def build_bundle(strategy: Dict[str, Any]) -> Dict[str, Any]:
    file_content = f"""
# AUTO-GENERATED REPAIR PATCH

def resolve_fork(children):
{strategy["code"]}
"""

    return {
        "proposal_name": strategy["name"],
        "files_to_create": [
            {
                "path": "engine/fork_resolution_patch.py",
                "content": file_content
            }
        ],
        "gaps": []
    }


# -------------------------
# MAIN ENTRY
# -------------------------

def proposal_to_bundle(snapshot: Dict[str, Any], failure_text: str) -> Dict[str, Any]:

    classification = classify_failure(failure_text)

    strategies = generate_strategies(classification["type"])

    if not strategies:
        return {
            "proposal_name": "no_op",
            "files_to_create": [],
            "gaps": ["unknown_failure_type"]
        }

    best = select_best_strategy(strategies)

    bundle = build_bundle(best)

    return bundle
