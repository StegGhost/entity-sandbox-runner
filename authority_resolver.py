import time
import hashlib
from typing import Dict, Any


class AuthorityResolver:
    def __init__(self) -> None:
        self.authority_registry: Dict[str, Dict[str, Any]] = {}

    def register_authority(
        self,
        authority_id: str,
        role: str,
        trust_score: float = 1.0,
    ) -> None:
        self.authority_registry[authority_id] = {
            "role": role,
            "trust_score": trust_score,
            "created_at": time.time(),
        }

    def resolve(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Supported proposal shapes:

        1.
        {
            "authority_id": "local_admin",
            ...
        }

        2.
        {
            "authority": {
                "authority_id": "local_admin"
            },
            ...
        }
        """
        authority_id = proposal.get("authority_id")

        if not authority_id:
            authority = proposal.get("authority", {})
            if isinstance(authority, dict):
                authority_id = authority.get("authority_id")

        if not authority_id:
            return {
                "valid": False,
                "reason": "missing_authority_id",
            }

        if authority_id not in self.authority_registry:
            return {
                "valid": False,
                "reason": "unknown_authority",
                "authority_id": authority_id,
            }

        authority = self.authority_registry[authority_id]

        return {
            "valid": True,
            "authority_id": authority_id,
            "authority": authority,
            "authority_hash": self.compute_authority_hash(authority_id),
        }

    def compute_authority_hash(self, authority_id: str) -> str:
        data = str(self.authority_registry.get(authority_id, {}))
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
