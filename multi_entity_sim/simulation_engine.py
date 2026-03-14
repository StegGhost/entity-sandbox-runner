class SimulationEngine:

    def __init__(self, entities):
        self.entities = entities
        self.step_count = 0

    def step(self):

        for e in self.entities:
            e.update_state()

        self.step_count += 1

    def run(self, steps=100):

        for _ in range(steps):
            self.step()
