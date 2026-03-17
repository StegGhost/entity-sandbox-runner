V8 governed system bundle

What it adds:
- deterministic enforcement layer
- receipt / audit logging
- multi-worker coordination
- economic weighting for U-signal and mode selection
- external signal adapter placeholder
- autonomous loop workflow update

iPhone-friendly note:
- workflow file is placed in `github_workflows/autonomous_loop.yml`
- move/copy it to `.github/workflows/autonomous_loop.yml` in the repo if needed

Primary files:
- experiments/evaluation_suite/run_eval.py
- install/deterministic_enforcer.py
- install/receipt_logger.py
- install/economic_weighting.py
- install/external_signal_adapter.py
- install/coordination.py
- payload/config/v8_policy.json
- github_workflows/autonomous_loop.yml
