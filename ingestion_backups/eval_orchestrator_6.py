# eval_orchestrator.py
# Wires scheduler + consensus + U-signal + governor

from install.adaptive_scheduler import add_shard, next_assignment
from install.quorum_consensus import quorum
from install.u_signal_integration import compute_U, classify
from install.stability_governor import decide

def seed_queue(shards):
    for s in shards:
        add_shard(s)

def run_cycle(workers):
    assignment = next_assignment(workers)
    if not assignment:
        return {"status": "idle"}

    worker_id = assignment.get("worker")
    shard = assignment.get("shard")

    # Simulate multi-worker results (can be replaced with real execution fan-out)
    results = ["ok", "ok", "fail"]

    decision = quorum(results)

    # Example signal inputs (replace with real telemetry when available)
    U = compute_U(1, 1, 1, 1)
    state = classify(U)

    action = decide(state)

    return {
        "assignment": {"worker": worker_id, "shard": shard},
        "decision": decision,
        "state": state,
        "action": action
    }
