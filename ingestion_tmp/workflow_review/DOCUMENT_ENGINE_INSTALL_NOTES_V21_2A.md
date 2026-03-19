# Document Engine Workflow Install Notes

This bootstrap bundle intentionally does **not** install `.github/workflows/document_engine.yml`
directly because the current ingestion hardening path rejects direct workflow installation.

Installed:
- engine files in `install/`
- config in `config/`

Staged for manual review:
- `workflow_review/DOCUMENT_ENGINE_WORKFLOW_V21_2A.yml.txt`

After this bundle installs, copy the reviewed YAML text into:
`.github/workflows/document_engine.yml`

Result:
- GitHub Actions popup will show dropdown choices for document generation.
