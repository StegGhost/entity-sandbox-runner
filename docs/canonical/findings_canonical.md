# Canonical Findings

1. # BUILD_NOTES Purpose: - Add automated evaluation workflow staging - Preserve ingestion-safe structure - Avoid root files and direct workflow injection during ingestion Expected result after promotion: - Repo gains `.github/workflows/run_evaluation.yml` - Evaluation can run automatically on qualifying pushes
   - sources: ingestion_backups/BUILD_NOTES_1.md, ingestion_backups/BUILD_NOTES_10.md, ingestion_backups/BUILD_NOTES_101.md, ingestion_backups/BUILD_NOTES_102.md, ingestion_backups/BUILD_NOTES_11.md
2. { "bundle_version": "1.0", "review_purpose": "SDK review and external packaging surface", "namespaces": { "results": { "description": "run-local raw outputs", "authoritative": false }, "receipts": { "description": "provenance reference layer", "authoritative": true }, "reports": { "description": "readable derived artifacts for inspection and download", "authoritative": false }, "data_records": { "description": "canonical machine-usable evidence used across experiments", "authoritative": true }, "manifests": { "description": "portable metadata for downstream ingest/export/sdk packaging", "authoritative": true } }, "sdk_download_surfaces": [ "reports/latest", "reports/visuals", "reports/validation", "data_records/aggregates", "manifests" ], "canonical_record_sets": [ "data_records/canonical/admissibility_observations.jsonl" ] }
   - sources: ingestion_backups/DEFINITIONS_REVIEW.json, sdk/DEFINITIONS_REVIEW.json
3. The experiment protocol can be rerun with explicit configuration and expected outputs.
   - sources: docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md, ingestion_backups/CLAIMS.md, ingestion_backups/CLAIMS_2.md, payload/docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md
4. The validation scripts can check deterministic and statistical output artifacts.
   - sources: docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md, ingestion_backups/CLAIMS.md, ingestion_backups/CLAIMS_2.md, payload/docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md
5. - The experiment protocol can be rerun with explicit configuration and expected outputs.
   - sources: docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md, ingestion_backups/CLAIMS.md, ingestion_backups/CLAIMS_2.md, payload/docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md
6. - The validation scripts can check deterministic and statistical output artifacts.
   - sources: docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md, ingestion_backups/CLAIMS.md, ingestion_backups/CLAIMS_2.md, payload/docs/demo_suite_suggestions/critical_ratio_campaign/CLAIMS.md
