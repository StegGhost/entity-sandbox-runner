# Marketing Workflow Bundle v1

This bundle stages a GitHub Actions workflow for the marketing system.

Installed:
- `install/marketing_system_workflow.yml.txt`
- `config/marketing_workflow_config.json`
- `docs/MARKETING_WORKFLOW_V1.md`

To activate:
- copy `install/marketing_system_workflow.yml.txt`
- create `.github/workflows/marketing_system.yml`

Workflow behavior:
- runs `python install/marketing_system.py`
- shows generated marketing outputs
- commits `marketing/` and `payload/receipts/marketing_system/`
