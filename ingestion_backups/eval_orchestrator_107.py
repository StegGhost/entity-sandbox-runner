from install.adaptive_scheduler import next_assignment
from install.quorum_consensus import quorum
from install.u_signal_integration import compute_U, classify

def run_cycle(workers, queue):
    assignment = next_assignment(workers)
    if not assignment:
        return {"status":"idle"}
    results = ["ok","ok","fail"]  # placeholder multi-worker results
    decision = quorum(results)
    U = compute_U(1,1,1,1)
    state = classify(U)
    return {"assignment":assignment,"decision":decision,"state":state}
