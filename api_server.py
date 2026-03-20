from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from decision_engine import decide, execute_if_allowed
from governed_executor import resolver
from llm_gateway import route_proposal, route_multi_proposal
from receipt_stream import get_receipts


app = FastAPI(title="StegVerse Decision Engine")


# ---- Models ----

class ProposalRequest(BaseModel):
    name: str
    authority_id: str
    payload: Optional[Dict[str, Any]] = None


class MultiProposalRequest(BaseModel):
    proposals: List[Dict[str, Any]]
    mode: str = "parallel"


# ---- Helpers ----

def build_proposal(req: ProposalRequest):
    def execute():
        return req.payload or {"ok": True}

    return {
        "name": req.name,
        "authority_id": req.authority_id,
        "payload": req.payload or {},
        "execute": execute,
    }


def resolve_authority(authority_id: str):
    return resolver.resolve(authority_id)


# ---- Routes ----

@app.get("/receipts")
def receipts():
    return get_receipts()


@app.post("/register_authority")
def register_authority(authority_id: str, role: str):
    resolver.register_authority(authority_id, role)
    return {"status": "registered"}


@app.post("/decide")
def decide_endpoint(req: ProposalRequest):
    proposal = build_proposal(req)
    authority = resolve_authority(req.authority_id)

    decision = decide(
        proposal=proposal,
        authority=authority,
    )

    return {"decision": decision}


@app.post("/execute")
def execute_endpoint(req: ProposalRequest):
    proposal = build_proposal(req)
    authority = resolve_authority(req.authority_id)

    result = execute_if_allowed(
        proposal=proposal,
        authority=authority,
    )

    return {"result": result}


@app.post("/propose")
def propose_endpoint(raw_input: Dict[str, Any]):
    """
    Canonical LLM entry point.
    Accepts a raw machine-generated proposal, normalizes it, resolves authority,
    decides, and executes if allowed.
    """
    return route_proposal(raw_input)


@app.post("/propose_multi")
def propose_multi_endpoint(req: MultiProposalRequest):
    """
    Multi-LLM / multi-agent orchestration entry point.
    Accepts multiple proposals and evaluates them in parallel.
    """
    return route_multi_proposal(req.proposals, mode=req.mode)
