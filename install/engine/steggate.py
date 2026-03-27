import time
import hashlib
import json
import threading
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

TOKENS = {}
TOKEN_LOCK = threading.Lock()
RECEIPT_FILE = "receipts.jsonl"

CONFIG = {
    "token_ttl_seconds": 120,
    "allowed_domains": [
        "httpbin.org"
    ],
    "max_payload_bytes": 10000,
    "rate_limit_per_token": 5,
    "http_timeout_seconds": 10
}


def _now():
    return int(time.time())


def _hash(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def issue_token():
    seed = f"{time.time()}::{len(TOKENS)}"
    token = hashlib.sha256(seed.encode("utf-8")).hexdigest()
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


def _policy_check(target, payload):
    parsed = urlparse(target)

    if parsed.scheme not in ("http", "https"):
        raise Exception("unsupported_scheme")

    if parsed.netloc not in CONFIG["allowed_domains"]:
        raise Exception("domain_not_allowed")

    payload_bytes = len(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )

    if payload_bytes > CONFIG["max_payload_bytes"]:
        raise Exception("payload_too_large")


def _execute_http(target, payload):
    body = json.dumps(payload).encode("utf-8")

    req = Request(
        target,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(req, timeout=CONFIG["http_timeout_seconds"]) as response:
            response_body = response.read().decode("utf-8", errors="replace")
            return {
                "status_code": getattr(response, "status", 200),
                "body": response_body[:1000]
            }

    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return {
            "status_code": e.code,
            "body": error_body[:1000]
        }

    except URLError as e:
        raise Exception(f"http_error:{e.reason}")

    except Exception as e:
        raise Exception(f"http_error:{str(e)}")


def _generate_receipt(action, target, payload, result):
    ts = _now()

    receipt = {
        "receipt_id": hashlib.sha256(f"{ts}:{target}:{_hash(payload)}".encode("utf-8")).hexdigest(),
        "timestamp": ts,
        "action": action,
        "target": target,
        "action_hash": _hash(payload),
        "result_hash": _hash(result),
        "policy_passed": True
    }

    with open(RECEIPT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(receipt, sort_keys=True) + "\n")

    return receipt


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
