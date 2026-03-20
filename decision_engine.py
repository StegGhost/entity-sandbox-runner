from typing import Dict, Any, Optional, List
import time
import copy

from receipt_chain_verifier import verify_chain
from multi_node_verifier import verify_nodes
from governed_executor import governed_execute


DEFAULT_NODE_DIR = "receipts"
DEFAULT_MULTI_NODES = ["receipts_node_a", "receipts_node_b"]


def _ensure_executable_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Backward-compatible adapter:
    - if 'name' is missing, derive it from 'action'
    - if 'execute' is missing, synthesize a deterministic callable
    """
    normalized = copy.copy(proposal)

    if "name" not in normalized or normalized.get("name") is None:
        normalized["name"] = normalized.get("action", "unnamed_proposal")

    if not callable(normalized.get("execute")):
        payload = normalized.get("payload")
        action = normalized.get("action", normalized.get("name"))

        def _default_execute():
            if isinstance(payload, dict):
                return payload
            return {"ok": True, "action": action}

        normalized["execute"] = _default_execute

    return normalized


def decide(
    proposal: Dict[str, Any],
    authority: Dict[str, Any],
    policy: Optional[Dict[str, Any]] = None,
    mode: str = "strict",
    node_dirs: Optional[List[str]] = None,
    receipt_dir: str = DEFAULT_NODE_DIR,
) -> Dict[str, Any]:
    timestamp = time.time()

    # 1. Authority check
    if not authority.get("valid", False):
        return {
            "allowed": False,
            "reason": "invalid_authority",
            "mode": mode,
            "timestamp": timestamp,
        }

    # 2. Local chain integrity
    chain_result = verify_chain(receipt_dir)
    if not chain_result.get("valid", False):
        return {
            "allowed": False,
            "reason": "chain_integrity_failure",
            "details": chain_result.get("reason"),
            "mode": mode,
            "timestamp": timestamp,
        }

    # 3. Multi-node consensus
    node_dirs = node_dirs or DEFAULT_MULTI_NODES
    consensus_result = verify_nodes(node_dirs)

    if mode == "strict":
        if not consensus_result.get("consensus", False):
            return {
                "allowed": False,
                "reason": "consensus_failure",
                "details": consensus_result,
                "mode": mode,
                "timestamp": timestamp,
            }

    elif mode == "economic":
        if not consensus_result.get("consensus_hash"):
            return {
                "allowed": False,
                "reason": "no_consensus_hash",
                "details": consensus_result,
                "mode": mode,
                "timestamp": timestamp,
            }

    # 4. Policy check
    if policy and policy.get("deny_all"):
        return {
            "allowed": False,
            "reason": "policy_denied",
            "mode": mode,
            "timestamp": timestamp,
        }

    return {
        "allowed": True,
        "reason": "approved",
        "mode": mode,
        "timestamp": timestamp,
        "consensus_hash": consensus_result.get("consensus_hash"),
        "confidence": consensus_result.get("confidence"),
    }


def execute_if_allowed(
    proposal: Dict[str, Any],
    authority: Dict[str, Any],
    policy: Optional[Dict[str, Any]] = None,
    mode: str = "strict",
    node_dirs: Optional[List[str]] = None,
    receipt_dir: str = DEFAULT_NODE_DIR,
) -> Dict[str, Any]:
    executable_proposal = _ensure_executable_proposal(proposal)

    decision = decide(
        proposal=executable_proposal,
        authority=authority,
        policy=policy,
        mode=mode,
        node_dirs=node_dirs,
        receipt_dir=receipt_dir,
    )

    if not decision.get("allowed", False):
        return {
            "status": "rejected",
            "decision": decision,
        }

    execution = governed_execute(
        proposal=executable_proposal,
        authority=authority,
        receipt_dir=receipt_dir,
    )

    if execution.get("status") != "committed":
        return {
            "status": "rejected",
            "decision": decision,
            "execution": execution,
        }

    return {
        "status": "committed",
        "decision": decision,
        "execution": execution,
    }
