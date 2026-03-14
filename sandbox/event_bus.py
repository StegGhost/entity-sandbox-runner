class EventBus:

    def __init__(self):
        self.events = []

    def emit(self, event):

        self.events.append(event)

    def consume(self):

        events = self.events
        self.events = []

        return events
