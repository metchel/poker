class EventStream:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def publish(self, event):
        for subscriber in self.subscribers:
            subscriber.on_event(event)
