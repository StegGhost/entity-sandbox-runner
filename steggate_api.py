from fastapi import FastAPI
from pydantic import BaseModel
import time
import hashlib
import json
from urllib.request import Request, urlopen
from urllib.parse import urlparse

app = FastAPI()

TOKENS = {}
CONFIG = {
    "ttl": 120,
    "allowed_domains": ["httpbin.org"]
}

def now():
    return int(time.time())

def hash_obj(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


# -------------------
# MODELS
# -------------------

class ExecuteRequest(BaseModel):
    target: str
    payload: dict


# -------------------
# TOKEN
# -------------------

@app.post("/token")
def issue_token():
    token = hashlib.sha256(str(time.time()).encode()).hexdigest()
    TOKENS[token] = now() + CONFIG["ttl"]
    return {"token": token, "expires_in": CONFIG["ttl"]}


def validate_token(token):
    if token not in TOKENS:
        raise Exception("invalid_token")
    if now() > TOKENS[token]:
        raise Exception("expired_token")


# -------------------
# EXECUTION
# -------------------

@app.post("/execute")
def execute(req: ExecuteRequest, token: str):
    validate_token(token)

    parsed = urlparse(req.target)
    if parsed.netloc not in CONFIG["allowed_domains"]:
        raise Exception("domain_not_allowed")

    body = json.dumps(req.payload).encode()

    request = Request(
        req.target,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request) as response:
        resp_body = response.read().decode()

    result = {
        "status_code": 200,
        "body": resp_body[:500]
    }

    receipt = {
        "receipt_id": hashlib.sha256(str(time.time()).encode()).hexdigest(),
        "timestamp": now(),
        "target": req.target,
        "action_hash": hash_obj(req.payload),
        "result_hash": hash_obj(result),
        "policy_passed": True
    }

    return {
        "status": "executed",
        "result": result,
        "receipt": receipt
    }
