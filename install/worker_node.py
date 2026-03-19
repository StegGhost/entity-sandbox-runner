class WorkerNode:
    def __init__(self, node_id):
        self.node_id = node_id

    def evaluate(self, proposal, compute_u, evaluate_stability):
        u = compute_u(proposal)
        decision = evaluate_stability(u)

        return {
            "node": self.node_id,
            "u": u,
            "decision": decision["action"]
        }
