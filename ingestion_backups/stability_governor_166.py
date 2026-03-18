
from decision_state_recorder import DecisionStateRecorder

class StabilityGovernor:
    def __init__(self, receipts_dir="receipts"):
        self.rec = DecisionStateRecorder(receipts_dir)

    def validate(self, delta, state):
        # placeholder for U-signal / BCAT
        return {"allowed": True, "reason": "pass"}

    def evaluate_and_commit(self, delta, state, authority, policy):
        v = self.validate(delta, state)
        if not v["allowed"]:
            raise Exception("BLOCKED")

        return self.rec.record(delta, state, authority, policy, v)
