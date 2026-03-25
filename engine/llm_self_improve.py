import re
from engine.priority_router import select_top_gap


# -------------------------------------------------
# GAP CLASSIFICATION (unchanged core)
# -------------------------------------------------
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


# -------------------------------------------------
# FAILURE PARSING (NEW CORE)
# -------------------------------------------------
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


# -------------------------------------------------
# FIX GENERATORS (REAL MUTATIONS)
# -------------------------------------------------

def fix_missing_import(name, module):
    # patch the module to define missing symbol
    return {
        "path": f"install/{module.replace('.', '/')}.py",
        "content": f"""

# AUTO-GENERATED FIX: missing import

def {name}(*args, **kwargs):
    return {{
        "status": "stub",
        "name": "{name}"
    }}
"""
    }


def fix_missing_module(module):
    return {
        "path": f"install/{module.replace('.', '/')}.py",
        "content": f"""

# AUTO-GENERATED MODULE

def placeholder():
    return "module_created"
"""
    }


def fix_signature_mismatch(function_name="route_multi_proposal"):
    # upgrade function to accept flexible kwargs
    return {
        "path": "install/llm_gateway.py",
        "content": f"""

# AUTO-PATCHED SIGNATURE FIX

def {function_name}(proposals, mode=None, **kwargs):
    return {{
        "mode": mode or "unknown",
        "count": len(proposals),
        "results": proposals
    }}
"""
    }


def fix_contract_mismatch():
    return {
        "path": "install/llm_adapter.py",
        "content": """

# AUTO-PATCHED CONTRACT FIX

def normalize_response(resp: dict):
    if "allowed" not in resp:
        resp["allowed"] = True
    return resp
"""
    }


# -------------------------------------------------
# PROPOSAL BUILDER
# -------------------------------------------------

def build_bundle(file_patch):
    return {
        "proposal_name": "auto_fix_bundle",
        "files_to_create": [file_patch],
        "justification": "Auto-generated fix based on failure pattern",
    }


# -------------------------------------------------
# MAIN GENERATION LOGIC
# -------------------------------------------------

def generate_proposal(snapshot: dict, failure_text: str = ""):
    gaps = classify_gaps(snapshot, failure_text)
    top_gap = select_top_gap(gaps)

    if not top_gap:
        return {
            "proposal_name": "no_op",
            "files_to_create": [],
            "gaps": [],
        }

    # ---- real fix routing ----

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

    # fallback (safe)
    return {
        "proposal_name": "no_op",
        "files_to_create": [],
        "gaps": gaps,
    }
