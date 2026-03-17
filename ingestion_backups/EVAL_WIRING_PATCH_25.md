# EVAL_WIRING_PATCH (v6.1)

Fixes:
- Wires scheduler queue into evaluation (seed_queue)
- Ensures run_cycle pulls from adaptive_scheduler queue
- Adds governor action output
- Adds metrics aggregation and summary

How to run:
- Ensure v6 bundle is installed (provides adaptive_scheduler, quorum_consensus, u_signal_integration)
- Run: python experiments/evaluation_suite/run_eval.py

Expected:
- Non-idle cycles with assignments
- Decision + state + action fields populated
- Final SUMMARY printed
