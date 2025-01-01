from unittest.mock import MagicMock

import pytest

from app.infrastructure import NullNotificationInfra, NotificationInfrastructure
from app.subscribers import MailSubscriber, Subscriber


class TestMailSubscriber:

    def test_init__sets_destination(self):
        subscriber = MailSubscriber(
            event_type="new_article",
            mail_to=["test@example.com"],
        )
        subscriber.infra = NullNotificationInfra()

        assert subscriber.destination == ["test@example.com"]
        assert subscriber.validate() is None

    def test_notify__calls_infra_send(self):
        subscriber = MailSubscriber(
            event_type="new_article", mail_to=["test@example.com"]
        )
        subscriber.infra = MagicMock(NotificationInfrastructure)
        subscriber.notify(
            destination="test@example.com", title="Test", message="Test message"
        )

        subscriber.infra.send.assert_called_once_with(
            destination="test@example.com", title="Test", content="Test message"
        )

    def test_notify__raises_exception_when_infra_is_not_set(self):
        subscriber = MailSubscriber(
            event_type="new_article",
            mail_to=["test@example.com"],
        )

        with pytest.raises(ValueError) as excinfo:
            subscriber.notify(
                destination="test@example.com",
                title="Test",
                message="Test message",
            )

    def test_get_event_type__returns_event_type(self):
        subscriber = MailSubscriber(
            event_type="new_article",
            mail_to=["test@example.com"],
        )

        assert subscriber.get_event_type() == "new_article"

    def test_get_subscriber_info__returns_subscriber_info(self):
        subscriber = MailSubscriber(
            event_type="new_article",
            mail_to=["test@example.com"],
        )

        assert subscriber.get_subscriber_info() == {
            "type": "mail",
            "email_to": ["test@example.com"],
        }
