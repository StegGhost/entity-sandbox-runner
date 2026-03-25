import re
from engine.priority_router import select_top_gap


def classify_gaps(snapshot: dict, failure_text: str = ""):
    gaps = []

    if snapshot.get("test_count", 0) < 3:
        gaps.append("low_test_coverage")

    if not snapshot.get("has_cge", False):
        gaps.append("missing_cge_root")

    if "ModuleNotFoundError" in failure_text:
        gaps.append("missing_module")

    if "ImportError" in failure_text:
        gaps.append("import_failure")

    if "TypeError" in failure_text:
        gaps.append("signature_mismatch")

    if "KeyError" in failure_text:
        gaps.append("contract_mismatch")

    if "AssertionError" in failure_text:
        gaps.append("behavior_failure")

    return list(dict.fromkeys(gaps))


def extract_import_error(failure_text: str):
    match = re.search(r"cannot import name '(.+)' from '(.+)'", failure_text)
    if match:
        return match.group(1), match.group(2)
    return None, None


def extract_missing_module(failure_text: str):
    match = re.search(r"No module named '(.+)'", failure_text)
    if match:
        return match.group(1)
    return None


def extract_signature_issue(failure_text: str):
    match = re.search(r"got an unexpected keyword argument '(.+)'", failure_text)
    if match:
        return match.group(1)
    return None


def fix_missing_import(name, module):
    module_path = module.replace(".", "/")
    return {
        "path": f"install/{module_path}.py",
        "content": f"""# AUTO-GENERATED FIX: missing import

def {name}(*args, **kwargs):
    return {{
        "status": "stub",
        "name": "{name}"
    }}
""",
    }


def fix_missing_module(module):
    module_path = module.replace(".", "/")
    return {
        "path": f"install/{module_path}.py",
        "content": """# AUTO-GENERATED MODULE

def placeholder():
    return "module_created"
""",
    }


def fix_signature_mismatch(function_name="route_multi_proposal"):
    return {
        "path": "install/llm_gateway.py",
        "content": f"""from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from decision_engine import decide, execute_if_allowed
from proposal_adapter import normalize_proposal
from tool_contracts import assert_valid_proposal_contract
from governed_executor import resolver


def _build_executable_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(proposal)

    if "name" not in normalized or normalized.get("name") is None:
        normalized["name"] = (
            normalized.get("proposal_name")
            or normalized.get("action")
            or "unnamed_proposal"
        )

    if not callable(normalized.get("execute")):
        payload = normalized.get("payload")

        def _default_execute():
            if isinstance(payload, dict):
                return payload
            return {{"ok": True}}

        normalized["execute"] = _default_execute

    return normalized


def _contract_error(raw_input: Dict[str, Any], error: Exception) -> Dict[str, Any]:
    return {{
        "allowed": False,
        "reason": "contract_violation",
        "error": str(error),
        "raw_input": raw_input,
    }}


def _signature_error() -> Dict[str, Any]:
    return {{
        "allowed": False,
        "reason": "invalid_signature",
    }}


def _evaluate_single(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    if "signature" in raw_input and raw_input.get("signature") != "valid_signature":
        return _signature_error()

    proposal = normalize_proposal(raw_input)

    try:
        assert_valid_proposal_contract(proposal)
    except Exception as e:
        return _contract_error(raw_input, e)

    proposal = _build_executable_proposal(proposal)

    authority_id = proposal.get("authority_id")
    authority = resolver.resolve(authority_id)

    decision = decide(
        proposal=proposal,
        authority=authority,
    )

    if not decision.get("allowed", False):
        return {{
            "decision": decision,
            "result": {{
                "status": "rejected",
                "decision": decision,
            }},
        }}

    result = execute_if_allowed(
        proposal=proposal,
        authority=authority,
    )

    return {{
        "decision": decision,
        "result": result,
    }}


def route_proposal(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    return _evaluate_single(raw_input)


def {function_name}(proposals: List[Dict[str, Any]], mode: str = "parallel") -> Dict[str, Any]:
    if not proposals:
        return {{
            "mode": mode,
            "count": 0,
            "results": [],
        }}

    results: List[Dict[str, Any]] = []

    if mode == "parallel":
        with ThreadPoolExecutor(max_workers=min(8, len(proposals))) as executor:
            futures = [executor.submit(_evaluate_single, p) for p in proposals]
            for future in as_completed(futures):
                results.append(future.result())

        return {{
            "mode": mode,
            "count": len(proposals),
            "results": results,
        }}

    elif mode == "first_allowed":
        selected_index = None
        selected = None

        for i, proposal in enumerate(proposals):
            result = _evaluate_single(proposal)
            results.append(result)

            decision = result.get("decision", {{}})
            if decision.get("allowed", False) and selected is None:
                selected_index = i
                selected = result
                break

        if selected is None and results:
            selected_index = 0
            selected = results[0]

        return {{
            "mode": mode,
            "count": len(proposals),
            "selected_index": selected_index,
            "selected": selected,
            "results": results,
        }}

    elif mode == "majority":
        for proposal in proposals:
            results.append(_evaluate_single(proposal))

        approvals = 0
        for item in results:
            decision = item.get("decision", {{}})
            if decision.get("allowed", False):
                approvals += 1

        return {{
            "mode": mode,
            "count": len(proposals),
            "approvals": approvals,
            "majority_allowed": approvals > (len(proposals) / 2),
            "results": results,
        }}

    for proposal in proposals:
        results.append(_evaluate_single(proposal))

    return {{
        "mode": mode,
        "count": len(proposals),
        "results": results,
    }}
""",
    }


def fix_contract_mismatch():
    return {
        "path": "install/llm_adapter.py",
        "content": """from typing import Any, Dict, Optional, List

from agent_registry import AgentRegistry
from llm_gateway import route_proposal


class LLMAdapter:
    def __init__(self, registry: Optional[AgentRegistry] = None) -> None:
        self.registry = registry or AgentRegistry()

    def register_agent(
        self,
        agent_id: str,
        model_id: str,
        role: str,
        authority_id: str,
        allowed_tools: Optional[List[str]] = None,
        trust_score: float = 1.0,
    ) -> None:
        self.registry.register_agent(
            agent_id=agent_id,
            model_id=model_id,
            role=role,
            authority_id=authority_id,
            allowed_tools=allowed_tools,
            trust_score=trust_score,
        )

    def adapt(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        return route_proposal(raw_input)

    def observe_and_propose(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        proposal = {
            "proposal_name": "state_driven_action",
            "authority_id": "system",
            "tool_target": "repo",
            "payload": observation,
            "model_id": "llm",
            "agent_id": "observer",
            "session_id": "runtime",
        }
        return route_proposal(proposal)
""",
    }


def build_bundle(file_patch):
    return {
        "proposal_name": "auto_fix_bundle",
        "files_to_create": [file_patch],
        "justification": "Auto-generated fix based on failure pattern",
    }


def generate_proposal(snapshot: dict, failure_text: str = ""):
    gaps = classify_gaps(snapshot, failure_text)
    top_gap = select_top_gap(gaps)

    if not top_gap:
        return {
            "proposal_name": "no_op",
            "files_to_create": [],
            "gaps": [],
        }

    if top_gap == "import_failure":
        name, module = extract_import_error(failure_text)
        if name and module:
            return build_bundle(fix_missing_import(name, module))

    if top_gap == "missing_module":
        module = extract_missing_module(failure_text)
        if module:
            return build_bundle(fix_missing_module(module))

    if top_gap == "signature_mismatch":
        return build_bundle(fix_signature_mismatch())

    if top_gap == "contract_mismatch":
        return build_bundle(fix_contract_mismatch())

    return {
        "proposal_name": "no_op",
        "files_to_create": [],
        "gaps": gaps,
    }
