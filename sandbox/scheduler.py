class Scheduler:

    def __init__(self, entities):
        self.entities = entities
        self.tick = 0

    def next_turn(self):

        entity = self.entities[self.tick % len(self.entities)]
        self.tick += 1

        return entity
