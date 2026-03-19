# Failure Recovery Bundle v1

Adds resilience to the autonomous loop.

Features:
- Retries per step (configurable)
- Exponential backoff
- Failure classification (missing_dependency, permission_error, data_corruption, timeout, unknown_error)
- Step isolation (can stop or continue on failure)
- Deterministic receipts + detailed report

Files:
- install/failure_recovery_runner.py
- config/failure_recovery_config.json
- docs/FAILURE_RECOVERY_V1.md

Run:
python install/failure_recovery_runner.py

Outputs:
- payload/runtime/failure_recovery_report.json
- payload/receipts/failure_recovery/failure_recovery_0001.json

Integration:
- Can replace orchestrator in workflow for resilient execution.
