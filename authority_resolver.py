import time
from typing import Dict, Any

class AuthorityResolver:
    def __init__(self):
        self.registry = {}

    def register_authority(self, authority_id: str, role: str, trust_score: float = 1.0):
        self.registry[authority_id] = {
            "role": role,
            "trust_score": trust_score,
            "created_at": time.time()
        }

    def resolve(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        authority_id = proposal.get("authority_id")
        if not authority_id:
            return {"valid": False, "reason": "missing_authority_id"}

        if authority_id not in self.registry:
            return {"valid": False, "reason": "unknown_authority"}

        return {
            "valid": True,
            "authority_id": authority_id,
            "authority": self.registry[authority_id]
        }