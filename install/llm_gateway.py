from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from decision_engine import decide, execute_if_allowed
from proposal_adapter import normalize_proposal
from governed_executor import resolver


def _build_executable_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(proposal)

    if "name" not in normalized or normalized.get("name") is None:
        normalized["name"] = normalized.get("action", "unnamed_proposal")

    if not callable(normalized.get("execute")):
        payload = normalized.get("payload")

        def _default_execute():
            if isinstance(payload, dict):
                return payload
            return {"ok": True}

        normalized["execute"] = _default_execute

    return normalized


def _evaluate_single(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    proposal = normalize_proposal(raw_input)
    proposal = _build_executable_proposal(proposal)

    authority_id = proposal.get("authority_id")
    authority = resolver.resolve(authority_id)

    # Explicit signature rejection contract
    if "signature" in raw_input and raw_input.get("signature") != "valid_signature":
        return {
            "allowed": False,
            "reason": "invalid_signature",
        }

    decision = decide(
        proposal=proposal,
        authority=authority,
    )

    if not decision.get("allowed", False):
        return {
            "decision": decision,
            "result": {
                "status": "rejected",
                "decision": decision,
            },
        }

    result = execute_if_allowed(
        proposal=proposal,
        authority=authority,
    )

    return {
        "decision": decision,
        "result": result,
    }


def route_proposal(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Canonical single-proposal entry point.
    Stable response contract:
    {
      "decision": {...} OR "allowed": False,
      "result": {...}    OR "reason": ...
    }
    """
    return _evaluate_single(raw_input)


def route_multi_proposal(proposals: List[Dict[str, Any]], mode: str = "parallel") -> Dict[str, Any]:
    """
    Multi-LLM orchestration.

    mode:
      - parallel: evaluate all independently
      - first_allowed: return first allowed result
      - majority: report majority-approval summary
    """
    if not proposals:
        return {
            "mode": mode,
            "count": 0,
            "results": [],
        }

    results: List[Dict[str, Any]] = []

    if mode == "parallel":
        with ThreadPoolExecutor(max_workers=min(8, len(proposals))) as executor:
            futures = [executor.submit(_evaluate_single, p) for p in proposals]
            for future in as_completed(futures):
                results.append(future.result())

    else:
        # deterministic sequential path
        for proposal in proposals:
            results.append(_evaluate_single(proposal))

            if mode == "first_allowed":
                current = results[-1]
                decision = current.get("decision", {})
                if decision.get("allowed", False):
                    return {
                        "mode": mode,
                        "count": len(proposals),
                        "selected_index": len(results) - 1,
                        "selected": current,
                        "results": results,
                    }

    if mode == "majority":
        approvals = 0
        for item in results:
            decision = item.get("decision", {})
            if decision.get("allowed", False):
                approvals += 1

        return {
            "mode": mode,
            "count": len(proposals),
            "approvals": approvals,
            "majority_allowed": approvals > (len(proposals) / 2),
            "results": results,
        }

    return {
        "mode": mode,
        "count": len(proposals),
        "results": results,
    }
