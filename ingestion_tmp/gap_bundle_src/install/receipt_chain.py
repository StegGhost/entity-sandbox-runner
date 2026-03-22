"""Hash-chained receipt store for governed agent execution."""

from __future__ import annotations

import json
import hashlib
import os
import time
from typing import Any, Dict, List


CHAIN_FILE = "receipts_chain.json"
GENESIS_HASH = "GENESIS"


def hash_data(data: Dict[str, Any]) -> str:
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_chain(chain_file: str = CHAIN_FILE) -> List[Dict[str, Any]]:
    if not os.path.exists(chain_file):
        return []
    with open(chain_file, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_chain(chain: List[Dict[str, Any]], chain_file: str = CHAIN_FILE) -> None:
    with open(chain_file, "w", encoding="utf-8") as handle:
        json.dump(chain, handle, indent=2, ensure_ascii=False)


def build_receipt(passport_hash: str, admission_result: Dict[str, Any], execution_result: Dict[str, Any], previous_hash: str) -> Dict[str, Any]:
    receipt = {
        "timestamp": time.time(),
        "passport_hash": passport_hash,
        "admission": admission_result,
        "execution": execution_result,
        "previous_hash": previous_hash,
    }
    receipt["receipt_hash"] = hash_data(receipt)
    return receipt


def append_receipt(passport_hash: str, admission_result: Dict[str, Any], execution_result: Dict[str, Any], chain_file: str = CHAIN_FILE) -> Dict[str, Any]:
    chain = load_chain(chain_file)
    previous_hash = chain[-1]["receipt_hash"] if chain else GENESIS_HASH
    receipt = build_receipt(passport_hash, admission_result, execution_result, previous_hash)
    chain.append(receipt)
    save_chain(chain, chain_file)
    return receipt
