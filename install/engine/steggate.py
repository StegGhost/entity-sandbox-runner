import time
import hashlib
import json
import threading
from urllib.parse import urlparse
import requests

# In-memory stores (v1 minimal)
TOKENS = {}
TOKEN_LOCK = threading.Lock()
RECEIPT_FILE = "receipts.jsonl"

CONFIG = {
    "token_ttl_seconds": 120,
    "allowed_domains": ["api.exchange.com", "httpbin.org"],
    "max_payload_bytes": 10_000,
    "rate_limit_per_token": 5
}

RATE_TRACK = {}


def _now():
    return int(time.time())


# -------------------------
# TOKEN VAULT
# -------------------------
def issue_token():
    token = hashlib.sha256(str(time.time()).encode()).hexdigest()
    expiry = _now() + CONFIG["token_ttl_seconds"]

    with TOKEN_LOCK:
        TOKENS[token] = {
            "expires": expiry,
            "count": 0
        }

    return {
        "token": token,
        "expires_in": CONFIG["token_ttl_seconds"]
    }


def _validate_token(token):
    with TOKEN_LOCK:
        data = TOKENS.get(token)

        if not data:
            raise Exception("invalid_token")

        if _now() > data["expires"]:
            raise Exception("expired_token")

        if data["count"] >= CONFIG["rate_limit_per_token"]:
            raise Exception("rate_limit_exceeded")

        data["count"] += 1


# -------------------------
# POLICY ENGINE
# -------------------------
def _policy_check(target, payload):
    parsed = urlparse(target)

    if parsed.netloc not in CONFIG["allowed_domains"]:
        raise Exception("domain_not_allowed")

    payload_bytes = len(json.dumps(payload).encode())

    if payload_bytes > CONFIG["max_payload_bytes"]:
        raise Exception("payload_too_large")


# -------------------------
# EXECUTION
# -------------------------
def _execute_http(target, payload):
    response = requests.post(target, json=payload, timeout=10)

    return {
        "status_code": response.status_code,
        "body": response.text[:1000]
    }


# -------------------------
# RECEIPTS
# -------------------------
def _hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def _generate_receipt(action, target, payload, result):
    ts = _now()

    receipt = {
        "receipt_id": hashlib.sha256(f"{ts}{target}".encode()).hexdigest(),
        "timestamp": ts,
        "action": action,
        "target": target,
        "action_hash": _hash(payload),
        "result_hash": _hash(result),
        "policy_passed": True
    }

    with open(RECEIPT_FILE, "a") as f:
        f.write(json.dumps(receipt) + "\n")

    return receipt


# -------------------------
# PUBLIC INTERFACE
# -------------------------
def validate_and_execute(action, target, payload, token):
    _validate_token(token)
    _policy_check(target, payload)

    result = _execute_http(target, payload)
    receipt = _generate_receipt(action, target, payload, result)

    return {
        "status": "executed",
        "result": result,
        "receipt": receipt
    }
