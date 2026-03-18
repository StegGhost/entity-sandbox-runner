# Architecture Map

## System Layers

1. Ingestion Layer
   - incoming_bundles/
   - ingestion_v2.py

2. Canonical Layer
   - payload/canonical_repo/

3. Preflight Layer
   - preflight_strict.py

4. Execution Layer
   - run_eval.py

5. Audit Layer
   - receipts/
   - logs/

## Flow

[Bundles] → [Ingestion] → [Canonical Sync] → [Preflight] → [Execution] → [Receipts]
