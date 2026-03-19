import hashlib
import time

class AuthorityResolver:
    def __init__(self):
        self.authority_registry = {}

    def register_authority(self, authority_id, role, trust_score=1.0):
        self.authority_registry[authority_id] = {
            "role": role,
            "trust_score": trust_score,
            "created_at": time.time()
        }

    def resolve(self, proposal):
        authority_id = proposal.get("authority_id")

        if authority_id not in self.authority_registry:
            return {
                "valid": False,
                "reason": "unknown_authority"
            }

        authority = self.authority_registry[authority_id]

        return {
            "valid": True,
            "authority": authority,
            "authority_id": authority_id
        }

    def compute_authority_hash(self, authority_id):
        data = str(self.authority_registry.get(authority_id, {}))
        return hashlib.sha256(data.encode()).hexdigest()
