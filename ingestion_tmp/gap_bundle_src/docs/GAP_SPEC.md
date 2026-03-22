# Governed Agent Passport (GAP) v1

GAP extends a signed agent passport into an execution-governance model.

## Core flow

1. Agent presents passport.
2. Proposed action is evaluated against declared capability and local policy.
3. If admitted, the action executes.
4. A receipt is created and chained into local history.

## Bundle contents

- `install/governed_passport.py`
- `install/admission_engine.py`
- `install/receipt_chain.py`
- `install/execution_wrapper.py`
- `config/authority_policy.json`

## Notes

- This bundle is dependency-light and intended for ingestion-friendly deployment.
- It provides structure, admission control, and receipt chaining.
- It does not include full Ed25519 signature verification for an external passport spec; that can be layered in next.
