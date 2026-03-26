import json
import os
import re
import time
from typing import Dict, Any, List

MEMORY_PATH = "brain_reports/failure_memory.json"


# =========================
# MEMORY LAYER
# =========================

def load_memory() -> Dict[str, Any]:
    if not os.path.exists(MEMORY_PATH):
        return {"known_failures": {}}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)


def save_memory(memory: Dict[str, Any]):
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)


def remember_failure(signature: str, classification: str):
    memory = load_memory()
    memory["known_failures"][signature] = {
        "classification": classification,
        "ts": time.time(),
    }
    save_memory(memory)


def recall_failure(signature: str) -> str:
    memory = load_memory()
    return memory["known_failures"].get(signature, {}).get("classification")


# =========================
# FAILURE CLASSIFICATION
# =========================

def extract_signature(failure_text: str) -> str:
    """
    Reduce failure text to a stable signature
    """
    lines = failure_text.strip().splitlines()
    for line in lines:
        if "ValueError" in line or "Exception" in line:
            return line.strip()
    return lines[-1] if lines else "unknown_failure"


def classify_failure(failure_text: str) -> str:
    signature = extract_signature(failure_text)

    # check memory first
    known = recall_failure(signature)
    if known:
        return known

    # === PATTERN DETECTION ===

    if "multiple children found" in failure_text:
        classification = "receipt_chain_fork"

    elif "cycle detected" in failure_text:
        classification = "receipt_cycle"

    elif "cannot import name" in failure_text:
        classification = "import_error"

    elif "missing_cge_root" in failure_text:
        classification = "cge_missing_root"

    elif "AssertionError" in failure_text:
        classification = "test_assertion_failure"

    else:
        classification = "unknown_failure"

    remember_failure(signature, classification)
    return classification


# =========================
# REPAIR STRATEGIES
# =========================

def repair_receipt_chain_fork() -> Dict[str, Any]:
    """
    Strategy:
    - enforce single-child rule
    - quarantine conflicting receipts
    """

    return {
        "proposal_name": "repair_receipt_chain_fork",
        "files_to_create": [
            {
                "path": "engine/receipt_fork_resolver.py",
                "content": '''
from typing import List, Dict, Any

def resolve_forks(receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_prev = {}

    for r in receipts:
        prev = r.get("previous_receipt_hash")
        by_prev.setdefault(prev, []).append(r)

    cleaned = []

    for prev, children in by_prev.items():
        if len(children) == 1:
            cleaned.append(children[0])
        else:
            # quarantine extras
            children.sort(key=lambda x: x.get("timestamp", 0))
            cleaned.append(children[0])

    return cleaned
'''
            }
        ],
        "quarantine": True,
    }


def repair_import_error() -> Dict[str, Any]:
    return {
        "proposal_name": "repair_import_error",
        "files_to_create": [],
        "notes": "Ensure module exports match imports"
    }


def repair_unknown() -> Dict[str, Any]:
    return {
        "proposal_name": "unknown_failure_analysis",
        "files_to_create": [
            {
                "path": "brain_reports/unknown_failure.log",
                "content": "Captured unknown failure for future learning\n"
            }
        ],
        "quarantine": True
    }


# =========================
# DISPATCH ENGINE
# =========================

def generate_repair_plan(classification: str) -> Dict[str, Any]:
    if classification == "receipt_chain_fork":
        return repair_receipt_chain_fork()

    elif classification == "import_error":
        return repair_import_error()

    else:
        return repair_unknown()


# =========================
# MAIN ENTRY
# =========================

def generate_proposal(snapshot: Dict[str, Any], failure_text: str = "") -> Dict[str, Any]:

    if not failure_text.strip():
        return {
            "status": "no_failure_input",
            "proposal": {
                "proposal_name": "no_op",
                "files_to_create": [],
                "gaps": []
            }
        }

    classification = classify_failure(failure_text)

    repair_plan = generate_repair_plan(classification)

    return {
        "status": "repair_generated",
        "classification": classification,
        "proposal": repair_plan
    }
