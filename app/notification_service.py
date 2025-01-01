from collections import defaultdict

from app.infrastructure import NotificationInfrastructure
from app.subscribers import Subscriber


class NotificationService:
    def __init__(self):
        self.subscribers: dict[str, list[Subscriber]] = defaultdict(list)
        self.infrastructures: dict[str, NotificationInfrastructure] = {}

    def register_infrastructure(
        self, subscriber_type: str, infrastructure: NotificationInfrastructure
    ):
        self.infrastructures[subscriber_type] = infrastructure

    def get_infrastructure(self, subscriber_type: str) -> NotificationInfrastructure:
        return self.infrastructures[subscriber_type]

    def add_subscriber(self, event_type: str, subscriber: Subscriber):
        subscriber_type = subscriber.__class__.__name__
        infrastructure = self.get_infrastructure(subscriber_type)
        subscriber.infra = infrastructure
        subscriber.validate()

        self.subscribers[event_type].append(subscriber)

    def notify(self, title: str, message: str):
        for event_type, subscribers in self.subscribers.items():
            for subscriber in subscribers:
                subscriber.notify(
                    destination=subscriber.destination, title=title, message=message
                )
