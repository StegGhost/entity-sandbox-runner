# V6.2 SHARED STATE PATCH

Fixes idle issue by introducing a single shared state module.

Changes:
- Added install/system_state.py (QUEUE, WORKERS, METRICS)
- Patched adaptive_scheduler to use shared QUEUE
- Patched eval_orchestrator to seed and consume same QUEUE
- Patched eval_metrics to use shared METRICS

Result:
- Scheduler and evaluation now operate on same state
- Idle condition eliminated when queue is seeded

No root files included (ingestion-safe).
