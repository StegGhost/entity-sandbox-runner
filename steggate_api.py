from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import time
import hashlib
import json
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError

app = FastAPI(title="StegGate API", version="0.1.0")

TOKENS = {}
RECEIPTS = {}

CONFIG = {
    "ttl": 120,
    "allowed_domains": [
        "httpbin.org"
    ],
    "http_timeout_seconds": 10
}


def now() -> int:
    return int(time.time())


def hash_obj(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


class ExecuteRequest(BaseModel):
    target: str
    payload: dict


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "steggate-api",
        "ts": now()
    }


@app.post("/token")
def issue_token():
    seed = f"{time.time()}::{len(TOKENS)}"
    token = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    TOKENS[token] = now() + CONFIG["ttl"]
    return {
        "status": "ok",
        "token": token,
        "expires_in": CONFIG["ttl"]
    }


def validate_token(token: str):
    expiry = TOKENS.get(token)
    if not expiry:
        raise HTTPException(status_code=401, detail="invalid_token")
    if now() > expiry:
        raise HTTPException(status_code=401, detail="expired_token")


def policy_check(target: str, payload: dict):
    parsed = urlparse(target)

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="unsupported_scheme")

    if parsed.netloc not in CONFIG["allowed_domains"]:
        raise HTTPException(status_code=403, detail="domain_not_allowed")

    payload_size = len(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )
    if payload_size > 10000:
        raise HTTPException(status_code=413, detail="payload_too_large")


def perform_http_post(target: str, payload: dict):
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
        raise HTTPException(status_code=502, detail=f"http_error:{e.reason}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"http_error:{str(e)}")


@app.post("/execute")
def execute(req: ExecuteRequest, token: str = Query(...)):
    validate_token(token)
    policy_check(req.target, req.payload)

    result = perform_http_post(req.target, req.payload)

    receipt = {
        "receipt_id": hashlib.sha256(
            f"{time.time()}::{req.target}::{hash_obj(req.payload)}".encode("utf-8")
        ).hexdigest(),
        "timestamp": now(),
        "target": req.target,
        "action_hash": hash_obj(req.payload),
        "result_hash": hash_obj(result),
        "policy_passed": True
    }

    RECEIPTS[receipt["receipt_id"]] = receipt

    return {
        "status": "executed",
        "result": result,
        "receipt": receipt
    }


@app.post("/verify")
def verify(receipt: dict):
    receipt_id = receipt.get("receipt_id")
    stored = RECEIPTS.get(receipt_id)

    if not stored:
        return {
            "valid": False,
            "reason": "receipt_not_found",
            "receipt_id": receipt_id
        }

    same = stored == receipt

    return {
        "valid": same,
        "reason": "ok" if same else "receipt_mismatch",
        "receipt_id": receipt_id
    }
