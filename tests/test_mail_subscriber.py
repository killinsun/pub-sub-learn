from unittest.mock import MagicMock

import pytest

from app.subscribers import MailSubscriber


class TestMailSubscriber:

    def test_get_event_type__returns_event_type(self):
        subscriber = MailSubscriber(
            event_type="new_article",
            mail_to=["test@example.com"],
            mail_client=None,
        )

        assert subscriber.get_event_type() == "new_article"

    def test_get_subscriber_info__returns_subscriber_info(self):
        subscriber = MailSubscriber(
            event_type="new_article",
            mail_to=["test@example.com"],
            mail_client=None,
        )

        assert subscriber.get_subscriber_info() == {
            "type": "mail",
            "email_to": ["test@example.com"],
        }

    def test_notify__calls_mail_api(self):
        mock_mail_client = MagicMock()

        subscriber = MailSubscriber(
            event_type="new_article",
            mail_to=["test@example.com"],
            mail_client=mock_mail_client,
        )

        subscriber.notify(title="Test", message="Test message")

        mock_mail_client.send_mail.assert_called_once_with(
            mail_from="no-reply@example.com",
            mail_to=["test@example.com"],
            subject="Test",
            body="Test message",
        )

    def test_notify__raises_exception_when_mail_to_is_empty(self):
        mock_mail_client = MagicMock()

        with pytest.raises(ValueError):
            MailSubscriber(mail_to=[], mail_client=mock_mail_client)
