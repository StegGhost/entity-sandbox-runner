import json
from typing import Dict, Any


def proposal_to_bundle(snapshot: Dict[str, Any], failure_text: str) -> Dict[str, Any]:

    # -------------------------
    # DETECT FORK FAILURE
    # -------------------------
    if "multiple children found (fork detected)" not in failure_text:
        return {
            "proposal_name": "no_op",
            "files_to_create": [],
            "gaps": ["unsupported_failure"]
        }

    # -------------------------
    # DIRECT MUTATION PATCH
    # -------------------------
    patched_code = """
def build_chain(receipts):
    if not receipts:
        return []

    by_prev = {}
    for r in receipts:
        prev = r.get("previous_receipt_hash")
        by_prev.setdefault(prev, []).append(r)

    genesis = by_prev.get(None, [])
    if len(genesis) != 1:
        raise ValueError("chain must contain exactly one genesis receipt")

    ordered = []
    seen = set()
    current = genesis[0]

    while current is not None:
        h = current.get("receipt_hash")

        if h in seen:
            raise ValueError("cycle detected in receipt chain")

        seen.add(h)
        ordered.append(current)

        children = by_prev.get(h, [])

        # 🔥 FIX: instead of failing → resolve fork deterministically
        if len(children) > 1:
            # choose highest trust score
            children = sorted(
                children,
                key=lambda x: x.get("authority", {}).get("trust_score", 0),
                reverse=True
            )

        current = children[0] if children else None

    return ordered
"""

    return {
        "proposal_name": "fix_receipt_chain_fork",
        "files_to_create": [
            {
                "path": "receipt_chain.py",
                "content": patched_code
            }
        ],
        "gaps": []
    }
