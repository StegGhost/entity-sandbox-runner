MODEL_SCORES = {}

def get_score(model_id: str) -> float:
    return MODEL_SCORES.get(model_id, 0.5)

def update_score(model_id: str, success: bool):
    current = MODEL_SCORES.get(model_id, 0.5)
    delta = 0.05 if success else -0.1
    MODEL_SCORES[model_id] = max(0.0, min(1.0, current + delta))
