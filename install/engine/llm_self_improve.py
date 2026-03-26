import json
import os
import time
from typing import Dict, Any, List

MEMORY_PATH = "brain_reports/failure_memory.json"


# =========================
# MEMORY
# =========================

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {"known_failures": {}}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)


def save_memory(memory):
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)


def extract_signature(failure_text: str) -> str:
    lines = failure_text.strip().splitlines()
    for line in lines:
        if "ValueError" in line or "Exception" in line:
            return line.strip()
    return lines[-1] if lines else "unknown_failure"


def classify_failure(failure_text: str) -> str:
    memory = load_memory()
    signature = extract_signature(failure_text)

    if signature in memory["known_failures"]:
        return memory["known_failures"][signature]["classification"]

    if "multiple children found" in failure_text:
        classification = "receipt_chain_fork"
    elif "cycle detected" in failure_text:
        classification = "receipt_cycle"
    elif "cannot import name" in failure_text:
        classification = "import_error"
    else:
        classification = "unknown_failure"

    memory["known_failures"][signature] = {
        "classification": classification,
        "ts": time.time()
    }
    save_memory(memory)

    return classification


# =========================
# MULTI-REPAIR GENERATION
# =========================

def repair_receipt_chain_fork_strict():
    return {
        "proposal_name": "fork_strict",
        "files_to_create": [
            {
                "path": "engine/receipt_chain_patch.py",
                "content": '''
def select_single_child(children):
    return sorted(children, key=lambda x: x.get("timestamp", 0))[0]
'''
            }
        ]
    }


def repair_receipt_chain_fork_prune():
    return {
        "proposal_name": "fork_prune",
        "files_to_create": [
            {
                "path": "engine/receipt_chain_patch.py",
                "content": '''
def select_single_child(children):
    return children[0]
'''
            }
        ]
    }


def repair_receipt_chain_fork_guard():
    return {
        "proposal_name": "fork_guard",
        "files_to_create": [
            {
                "path": "engine/receipt_chain_patch.py",
                "content": '''
def select_single_child(children):
    if len(children) > 1:
        return children[0]
    return children[0]
'''
            }
        ]
    }


def generate_repair_candidates(classification: str) -> List[Dict[str, Any]]:
    if classification == "receipt_chain_fork":
        return [
            repair_receipt_chain_fork_strict(),
            repair_receipt_chain_fork_prune(),
            repair_receipt_chain_fork_guard()
        ]

    return [{
        "proposal_name": "noop",
        "files_to_create": []
    }]


# =========================
# ENTRY
# =========================

def generate_proposals(snapshot: Dict[str, Any], failure_text: str = ""):

    if not failure_text.strip():
        return {
            "status": "no_failure",
            "proposals": []
        }

    classification = classify_failure(failure_text)

    proposals = generate_repair_candidates(classification)

    return {
        "status": "candidates_generated",
        "classification": classification,
        "proposals": proposals
    }
