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
    elif "missing_cge_root" in failure_text:
        classification = "cge_missing_root"
    elif "AssertionError" in failure_text:
        classification = "test_assertion_failure"
    else:
        classification = "unknown_failure"

    memory["known_failures"][signature] = {
        "classification": classification,
        "ts": time.time()
    }
    save_memory(memory)

    return classification


# =========================
# REPAIRS
# =========================

def repair_receipt_chain_fork():
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
            children.sort(key=lambda x: x.get("timestamp", 0))
            cleaned.append(children[0])

    return cleaned
'''
            }
        ]
    }


def repair_unknown():
    return {
        "proposal_name": "unknown_failure",
        "files_to_create": [
            {
                "path": "brain_reports/unknown_failure.log",
                "content": "Unknown failure captured\n"
            }
        ]
    }


def generate_repair_plan(classification: str):
    if classification == "receipt_chain_fork":
        return repair_receipt_chain_fork()
    else:
        return repair_unknown()


# =========================
# ENTRY
# =========================

def generate_proposal(snapshot: Dict[str, Any], failure_text: str = ""):

    if not failure_text.strip():
        return {
            "status": "no_failure",
            "proposal": {
                "proposal_name": "no_op",
                "files_to_create": [],
                "gaps": []
            }
        }

    classification = classify_failure(failure_text)

    repair = generate_repair_plan(classification)

    return {
        "status": "repair_generated",
        "classification": classification,
        "proposal": repair
    }
