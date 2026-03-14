class AdversaryAgent:

    def __init__(self, entity):
        self.entity = entity

    def attack(self, target):

        # increase artifact pressure of target
        target.artifact_pressure += 0.1
