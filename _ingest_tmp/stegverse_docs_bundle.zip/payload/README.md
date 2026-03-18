# StegVerse Entity Sandbox Runner

## Overview
Self-governing, self-healing execution system.

FLOW:
INGEST → PREPARE → VERIFY → HEAL → LOCK → EXECUTE → RECORD

## Components
- ingestion_v2.py
- preflight_strict.py
- run_eval.py
- canonical_repo
- receipts + audit logs

## Guarantees
- deterministic execution
- auto-repair
- auditability

## Run
export PYTHONPATH=$PYTHONPATH:$(pwd)
python experiments/evaluation_suite/run_eval.py
