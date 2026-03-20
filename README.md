# StegVerse Governed Execution + LLM Adapter Layer

This repository now supports an **LLM-agnostic proposal adapter layer** on top of the governed execution and decision engine system.

## What this adds

The adapter layer treats any LLM, agent framework, planner, or external reasoning system as a **proposal source** rather than an authority source.

That means:

- LLM output does **not** directly execute actions
- LLM output becomes a **proposal request**
- the decision engine evaluates admissibility before execution
- the governed executor records the result with receipts and chain integrity

## Core model

The architecture is:

```text
LLM(s) / Agents / Planners
        ↓
proposal_adapter.py
        ↓
llm_gateway.py
        ↓
decision_engine.py
        ↓
governed_executor.py
        ↓
receipts / state reconstruction / multi-node verification
```

## Design principle

The system is intentionally **LLM-agnostic**.

Any model can connect if it can emit a structured proposal with the required fields.

Examples:

- OpenAI tools / Responses API clients
- Anthropic tool-use agents
- local open-weight models
- AutoGen / LangGraph / CrewAI style orchestrators
- scripted automation systems

## Authority model

Authority is not granted by the LLM itself.

Authority is resolved through the governed execution layer.

A model may act as:

- proposer
- planner
- critic
- reviewer
- explainer

But the **execution boundary** still belongs to the governed system.

## New files

### `tool_contracts.py`
Defines canonical proposal schema requirements and validation helpers.

### `agent_registry.py`
Stores agent metadata including model identity, roles, allowed tools, and trust level.

### `proposal_adapter.py`
Normalizes raw model output into a canonical proposal contract the decision engine can evaluate.

### `llm_adapter.py`
High-level adapter that converts model output into governed execution proposals.

### `llm_gateway.py`
Receives normalized LLM requests, validates them, checks policy + authority context, and returns a ready proposal package.

### `test_llm_adapter.py`
Validates registry + adapter + gateway behavior.

### `.github/workflows/llm_adapter_validation.yml`
Runs validation tests in CI.

## Canonical proposal contract

The adapter layer uses this structure:

```json
{
  "model_id": "gpt-5.x",
  "agent_id": "agent_ops",
  "session_id": "session-123",
  "proposal_name": "update_customer_record",
  "authority_id": "local_admin",
  "tool_target": "records.update",
  "payload": {
    "customer_id": "123",
    "status": "active"
  },
  "justification": "Customer status correction requested by authorized workflow.",
  "confidence": 0.86,
  "state_claims": {
    "expected_record_exists": true
  }
}
```

## Simultaneous multi-LLM support

Yes, multiple LLMs can connect simultaneously.

The intended pattern is:

- each LLM uses its own `model_id`
- each logical actor uses its own `agent_id`
- each request carries its own `session_id`
- authority is resolved independently of model origin
- proposals are receipted independently

This enables:

- parallel proposal generation
- ensemble planning
- planner / critic / executor separation
- multi-model comparison before execution

## Recommended integration sequence

1. Register agents in `agent_registry.py`
2. Convert raw LLM output with `proposal_adapter.py`
3. Route normalized proposal through `llm_gateway.py`
4. Pass approved proposal into `decision_engine.py`
5. Execute through `governed_executor.py`
6. Persist receipts + verify state / consensus

## Installation notes

This bundle is designed to be ingested as a folder-mapped update.

Replace or add the included files at repository root:

- `README.md`
- `tool_contracts.py`
- `agent_registry.py`
- `proposal_adapter.py`
- `llm_adapter.py`
- `llm_gateway.py`
- `test_llm_adapter.py`
- `.github/workflows/llm_adapter_validation.yml`

## Next recommended build after this bundle

- signed agent identities
- tool-level policy modules
- API routes for `/propose`, `/decide`, `/execute`
- OpenAI / Anthropic request adapters
- conflict detection for simultaneous proposals against shared state

## Category framing

This is not just an agent wrapper.

It is an **execution-bound governance interface for machine-generated action**.
