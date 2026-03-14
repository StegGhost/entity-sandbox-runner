class EntityState:

    def __init__(self, state):
        self.state = state

    def update(self, new_state):

        self.state = new_state

    def snapshot(self):

        return dict(self.state)
