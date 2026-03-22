Trajectory-aware retry selection v10

Contents:
- .github/workflows/self_improving_governed_loop.yml
- engine/trajectory_retry_selector_v10.py

Purpose:
- Select retry behavior based on both ingestion failure class and recent receipt trajectory risk.
- Prevent unsafe auto-retries when system drift is already high.
