# StegVerse Entity Sandbox Runner

A governed, self-healing execution environment for deterministic experiments.

## Core flow

INGEST → PREFLIGHT → HEAL → EXECUTE → RECORD

## What this repo does

- processes bundles from `incoming_bundles/`
- validates repo state against canonical expectations
- repairs drift before execution
- runs experiments under controlled policy
- writes receipts and audit records for reproducibility

## Primary system areas

- `install/` — ingestion, preflight, integrity, policy, and support engines
- `experiments/evaluation_suite/` — execution entrypoints
- `config/` — experiment profiles and policy
- `payload/receipts/` — continuous execution receipts
- `payload/integrity/` — integrity and preflight artifacts
- `payload/canonical_repo/` — canonical repo state used for repair
- `incoming_bundles/` / `installed_bundles/` / `failed_bundles/` — governed bundle flow

## Operating model

### Continuous mode
Default append-only ledger for all governed activity.

### Experiment mode
User-scoped session layered on top of continuous mode.

### Replay mode
User-scoped reproducibility lane layered on top of continuous mode.

## Execution rule

Only verified, reproducible repo states are allowed to execute.
