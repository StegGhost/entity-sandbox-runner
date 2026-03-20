# Canonical Feedback

- summary_hash: 02309cde4ffa522137791a7bdc597d4a8cd0003b630a40652632a20ddf943aed
- claims_count: 12
- definitions_count: 8
- findings_count: 12
- feedback_hash: 5e748f0675b621e2c7f52fa69a8ccd8350b4597099e2af6ab871a83033b74184

## Priority Items
- { "bundle_version": "1.0", "review_purpose": "SDK review and external packaging surface", "namespaces": { "results": { "description": "run-local raw outputs", "authoritative": false }, "receipts": { "description": "provenance reference layer", "authoritative": true }, "reports": { "description": "readable derived artifacts for inspection and download", "authoritative": false }, "data_records": { "description": "canonical machine-usable evidence used across experiments", "authoritative": true }, "manifests": { "description": "portable metadata for downstream ingest/export/sdk packaging", "authoritative": true } }, "sdk_download_surfaces": [ "reports/latest", "reports/visuals", "reports/validation", "data_records/aggregates", "manifests" ], "canonical_record_sets": [ "data_records/canonical/admissibility_observations.jsonl" ] }
- # Claims ## Proven by demo - The critical ratio campaign computes the candidate invariant `U` as specified.
- # Claims ## Proven by demo - The experiment computes the candidate invariant U exactly as specified.
- sources: docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md, ingestion_backups/CLAIMS.md, ingestion_backups/CLAIMS_2.md, payload/docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md
- The critical ratio campaign computes the candidate invariant `U` as specified.
- The experiment computes the candidate invariant U exactly as specified.
- The candidate invariant can be compared against simpler baseline ratios.
- ## Supported by demo - The candidate invariant can be compared against simpler baseline ratios.
- Evaluation bundle: - orchestrated run cycle - quorum + U-signal integration - stability governor decisions - metrics collection Run experiments/evaluation_suite/run_eval.py to validate system behavior.
- # BUILD_NOTES Purpose: - Add automated evaluation workflow staging - Preserve ingestion-safe structure - Avoid root files and direct workflow injection during ingestion Expected result after promotion: - Repo gains `.github/workflows/run_evaluation.yml` - Evaluation can run automatically on qualifying pushes
- The validation scripts can check deterministic and statistical output artifacts.
- - The validation scripts can check deterministic and statistical output artifacts.
- sources: ingestion_backups/EVAL_NOTES_1.md, ingestion_backups/EVAL_NOTES_10.md, ingestion_backups/EVAL_NOTES_100.md, ingestion_backups/EVAL_NOTES_101.md, ingestion_backups/EVAL_NOTES_102.md
- sources: ingestion_backups/BUILD_NOTES_100.md, ingestion_backups/BUILD_NOTES_103.md, ingestion_backups/BUILD_NOTES_104.md, ingestion_backups/BUILD_NOTES_105.md, ingestion_backups/BUILD_NOTES_106.md
- sources: ingestion_backups/BUILD_NOTES_1.md, ingestion_backups/BUILD_NOTES_10.md, ingestion_backups/BUILD_NOTES_101.md, ingestion_backups/BUILD_NOTES_102.md, ingestion_backups/BUILD_NOTES_11.md

## Invariant Candidates
- { "bundle_version": "1.0", "review_purpose": "SDK review and external packaging surface", "namespaces": { "results": { "description": "run-local raw outputs", "authoritative": false }, "receipts": { "description": "provenance reference layer", "authoritative": true }, "reports": { "description": "readable derived artifacts for inspection and download", "authoritative": false }, "data_records": { "description": "canonical machine-usable evidence used across experiments", "authoritative": true }, "manifests": { "description": "portable metadata for downstream ingest/export/sdk packaging", "authoritative": true } }, "sdk_download_surfaces": [ "reports/latest", "reports/visuals", "reports/validation", "data_records/aggregates", "manifests" ], "canonical_record_sets": [ "data_records/canonical/admissibility_observations.jsonl" ] }
- # Claims ## Proven by demo - The critical ratio campaign computes the candidate invariant `U` as specified.
- # Claims ## Proven by demo - The experiment computes the candidate invariant U exactly as specified.
- The critical ratio campaign computes the candidate invariant `U` as specified.
- The experiment computes the candidate invariant U exactly as specified.
- The candidate invariant can be compared against simpler baseline ratios.
- ## Supported by demo - The candidate invariant can be compared against simpler baseline ratios.
- The validation scripts can check deterministic and statistical output artifacts.
- - The validation scripts can check deterministic and statistical output artifacts.

## Contradictions
- none detected by current marker rules

## Recommended Next Actions
- Feed invariant_candidates into formal document generation.
- Bind summary_hash into future receipts.
- Track delta between previous and current canonical summaries.
- Review contradictions before auto-promotion into policy.