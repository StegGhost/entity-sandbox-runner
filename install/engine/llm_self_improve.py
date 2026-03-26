import json
import os
import time
import hashlib
from typing import Dict, Any, List

MEMORY_PATH = "brain_reports/failure_memory.json"


# =========================
# MEMORY SYSTEM
# =========================

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {"failures": {}, "strategies": {}}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)


def save_memory(mem):
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    with open(MEMORY_PATH, "w") as f:
        json.dump(mem, f, indent=2)


def signature(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# =========================
# CLASSIFICATION
# =========================

def classify_failure(failure_text: str) -> str:
    mem = load_memory()
    sig = signature(failure_text)

    if sig in mem["failures"]:
        return mem["failures"][sig]["class"]

    if "multiple children found" in failure_text:
        cls = "receipt_chain_fork"
    elif "cycle detected" in failure_text:
        cls = "receipt_cycle"
    elif "ImportError" in failure_text or "cannot import" in failure_text:
        cls = "import_error"
    elif "AssertionError" in failure_text:
        cls = "test_failure"
    else:
        cls = "unknown"

    mem["failures"][sig] = {"class": cls, "ts": time.time()}
    save_memory(mem)
    return cls


# =========================
# STRATEGY LIBRARY (EXPANDABLE)
# =========================

def strategies_for(classification: str) -> List[Dict[str, Any]]:

    if classification == "receipt_chain_fork":
        return [
            {
                "name": "fork_strict",
                "files": [{
                    "path": "engine/receipt_chain_patch.py",
                    "content": "def select_child(children): return sorted(children, key=lambda x: x.get('timestamp',0))[0]\n"
                }]
            },
            {
                "name": "fork_first",
                "files": [{
                    "path": "engine/receipt_chain_patch.py",
                    "content": "def select_child(children): return children[0]\n"
                }]
            },
            {
                "name": "fork_guard",
                "files": [{
                    "path": "engine/receipt_chain_patch.py",
                    "content": "def select_child(children): return children[0] if children else None\n"
                }]
            }
        ]

    if classification == "import_error":
        return [{
            "name": "import_stub",
            "files": [{
                "path": "engine/import_stub.py",
                "content": "# stub to satisfy import\n"
            }]
        }]

    return [{
        "name": "noop",
        "files": []
    }]


# =========================
# ENTRY
# =========================

def generate_proposals(snapshot: Dict[str, Any], failure_text: str = ""):

    if not failure_text.strip():
        return {
            "status": "no_failure",
            "classification": None,
            "proposals": []
        }

    cls = classify_failure(failure_text)
    proposals = strategies_for(cls)

    return {
        "status": "ok",
        "classification": cls,
        "proposals": proposals
    }
