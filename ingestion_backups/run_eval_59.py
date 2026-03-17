# run_eval.py
# Entry point for evaluation (uses scheduler + orchestrator)

import json
from install.eval_orchestrator import run_cycle, seed_queue
from install.eval_metrics import record, summary

# Load config
with open("payload/config/eval_config.json", "r") as f:
    cfg = json.load(f)

# Mock workers (scores feed scheduler selection)
workers = {
    "w1": {"score": 1.0},
    "w2": {"score": 0.9}
}

# Seed scheduler queue
seed_queue(cfg.get("seed_shards", []))

# Run cycles
for _ in range(cfg.get("cycles", 2)):
    out = run_cycle(workers)
    print(out)
    if out.get("status") != "idle":
        record(out)

print("SUMMARY:", summary())
