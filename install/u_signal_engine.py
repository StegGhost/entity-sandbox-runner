from llm_weighting import get_score

def compute_u_signal(proposal: dict, context: dict = None) -> float:
    """
    U = system stability signal (0 → unstable, 1 → stable)
    """

    model_id = proposal.get("model_id", "unknown")
    trust = get_score(model_id)

    disagreement_penalty = context.get("disagreement", 0.0) if context else 0.0
    error_penalty = context.get("error_rate", 0.0) if context else 0.0

    u = trust - (0.3 * disagreement_penalty) - (0.5 * error_penalty)

    return max(0.0, min(1.0, u))
