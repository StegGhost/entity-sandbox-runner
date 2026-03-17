# BUILD_NOTES

Purpose:
- Add automated evaluation workflow staging
- Preserve ingestion-safe structure
- Avoid root files and direct workflow injection during ingestion

Expected result after promotion:
- Repo gains `.github/workflows/run_evaluation.yml`
- Evaluation can run automatically on qualifying pushes
