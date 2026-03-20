from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional

from decision_engine import decide, execute_if_allowed
from governed_executor import resolver

app = FastAPI(title="StegVerse Decision Engine")

# ---- Models ----

class ProposalRequest(BaseModel):
    name: str
    authority_id: str
    payload: Optional[Dict[str, Any]] = None


# ---- Helpers ----

def build_proposal(req: ProposalRequest):
    def execute():
        return req.payload or {"ok": True}

    return {
        "name": req.name,
        "authority_id": req.authority_id,
        "execute": execute,
    }


def resolve_authority(authority_id: str):
    return resolver.resolve(authority_id)


# ---- Routes ----

@app.post("/register_authority")
def register_authority(authority_id: str, role: str):
    resolver.register_authority(authority_id, role)
    return {"status": "registered"}


@app.post("/decide")
def decide_endpoint(req: ProposalRequest):
    proposal = build_proposal(req)
    authority = resolve_authority(req.authority_id)

    decision = decide(proposal, authority)

    return {"decision": decision}


@app.post("/execute")
def execute_endpoint(req: ProposalRequest):
    proposal = build_proposal(req)

    result = execute_if_allowed(proposal)

    return {"result": result}
