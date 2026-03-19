# System Summary

- scanned_files_count: 325
- claims_count: 6
- definitions_count: 4
- findings_count: 6
- summary_hash: 02309cde4ffa522137791a7bdc597d4a8cd0003b630a40652632a20ddf943aed

## Top Claims
- # Claims ## Proven by demo - The critical ratio campaign computes the candidate invariant `U` as specified.
- # Claims ## Proven by demo - The experiment computes the candidate invariant U exactly as specified.
- The critical ratio campaign computes the candidate invariant `U` as specified.
- The experiment computes the candidate invariant U exactly as specified.
- The candidate invariant can be compared against simpler baseline ratios.
- ## Supported by demo - The candidate invariant can be compared against simpler baseline ratios.

## Top Definitions
- ## Not yet proven - Real-world universality across domains - External validity beyond the sandbox model family - Full physical-law generalization
- Evaluation bundle: - orchestrated run cycle - quorum + U-signal integration - stability governor decisions - metrics collection Run experiments/evaluation_suite/run_eval.py to validate system behavior.
- External validity beyond the sandbox model family
- # BUILD_NOTES This bundle is designed for a no-CLI workflow.

## Top Findings
- # BUILD_NOTES Purpose: - Add automated evaluation workflow staging - Preserve ingestion-safe structure - Avoid root files and direct workflow injection during ingestion Expected result after promotion: - Repo gains `.github/workflows/run_evaluation.yml` - Evaluation can run automatically on qualifying pushes
- { "bundle_version": "1.0", "review_purpose": "SDK review and external packaging surface", "namespaces": { "results": { "description": "run-local raw outputs", "authoritative": false }, "receipts": { "description": "provenance reference layer", "authoritative": true }, "reports": { "description": "readable derived artifacts for inspection and download", "authoritative": false }, "data_records": { "description": "canonical machine-usable evidence used across experiments", "authoritative": true }, "manifests": { "description": "portable metadata for downstream ingest/export/sdk packaging", "authoritative": true } }, "sdk_download_surfaces": [ "reports/latest", "reports/visuals", "reports/validation", "data_records/aggregates", "manifests" ], "canonical_record_sets": [ "data_records/canonical/admissibility_observations.jsonl" ] }
- The experiment protocol can be rerun with explicit configuration and expected outputs.
- The validation scripts can check deterministic and statistical output artifacts.
- - The experiment protocol can be rerun with explicit configuration and expected outputs.
- - The validation scripts can check deterministic and statistical output artifacts.