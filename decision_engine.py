from typing import Dict, Any, Optional
import time

from receipt_chain_verifier import verify_chain
from multi_node_verifier import verify_nodes
from state_reconstructor import reconstruct_state


DEFAULT_NODE_DIR = "receipts"
DEFAULT_MULTI_NODES = ["receipts_node_a", "receipts_node_b"]


def decide(
    proposal: Dict[str, Any],
    authority: Dict[str, Any],
    policy: Optional[Dict[str, Any]] = None,
    mode: str = "strict",
    node_dirs: Optional[list] = None,
) -> Dict[str, Any]:

    timestamp = time.time()

    # 1. Authority check
    if not authority.get("valid"):
        return {
            "allowed": False,
            "reason": "invalid_authority",
            "mode": mode,
            "timestamp": timestamp,
        }

    # 2. Chain integrity
    chain_result = verify_chain(DEFAULT_NODE_DIR)
    if chain_result.get("status") != "ok":
        return {
            "allowed": False,
            "reason": "chain_integrity_failure",
            "mode": mode,
            "timestamp": timestamp,
        }

    # 3. Multi-node consensus
    node_dirs = node_dirs or DEFAULT_MULTI_NODES
    consensus_result = verify_nodes(node_dirs)

    if mode == "strict":
        if not consensus_result["consensus"]:
            return {
                "allowed": False,
                "reason": "consensus_failure",
                "mode": mode,
                "timestamp": timestamp,
            }

    elif mode == "economic":
        if not consensus_result.get("consensus_hash"):
            return {
                "allowed": False,
                "reason": "no_consensus_hash",
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
    }


def execute_if_allowed(
    proposal: Dict[str, Any],
    authority: Dict[str, Any],
    policy: Optional[Dict[str, Any]] = None,
    mode: str = "strict",
) -> Dict[str, Any]:

    decision = decide(proposal, authority, policy, mode)

    if not decision["allowed"]:
        return {
            "status": "rejected",
            "decision": decision,
        }

    # 🔥 Replace governed_execute with simple deterministic execution
    # This mirrors your existing system behavior safely

    result = {
        "ok": True,
        "proposal": proposal,
        "authority": authority,
    }

    return {
        "status": "committed",
        "decision": decision,
        "execution": result,
    }
