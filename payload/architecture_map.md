# Architecture Map v2

## Lifecycle

INGEST → CANONICAL ALIGN → PREFLIGHT → EXECUTE → RECORD

## Key Systems

- ingestion_v2.py → installs bundles
- preflight_strict.py → enforces correctness
- run_eval.py → executes experiments
- receipt chain → audit + reproducibility

## Hash Enforcement

- canonical hash required before execution
- mismatch triggers repair
- recorded in receipt
