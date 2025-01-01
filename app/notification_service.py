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
        """
        NotificationInfrastructure を実装したクラスを登録する。

        :param subscriber_type: str Subscriber タイプ。主に名前
        :param infrastructure: NotificationInfrastructure NotificationInfrastructure を実装したクラス
        :return:
        """

        self.infrastructures[subscriber_type] = infrastructure

    def get_infrastructure(self, subscriber_type: str) -> NotificationInfrastructure:
        return self.infrastructures[subscriber_type]

    def add_subscriber(self, event_type: str, subscriber: Subscriber):
        """
        Subscriber を登録する。
        subscriber_type に対応する NotificationInfrastructure を register_infrastructure で登録する必要がある

        :param event_type: str イベントタイプ
        :param subscriber: Subscriber 登録する Subscriber インスタンス
        :return:
        """
        subscriber_type = subscriber.__class__.__name__
        infrastructure = self.get_infrastructure(subscriber_type)
        subscriber.infra = infrastructure
        subscriber.validate()

        self.subscribers[event_type].append(subscriber)

    def notify(self, title: str, message: str):
        """
        登録されている Subscriber に通知を送信する
        :param title: str 通知タイトル
        :param message: str メッセージ本文
        :return:
        """

        for event_type, subscribers in self.subscribers.items():
            for subscriber in subscribers:
                subscriber.notify(
                    destination=subscriber.destination, title=title, message=message
                )
