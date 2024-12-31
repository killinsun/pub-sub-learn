from unittest.mock import MagicMock

import pytest

from app.subscribers import MailSubscriber


class TestMailSubscriber:

    def test_notify__calls_mail_api(self):
        mock_mail_client = MagicMock()

        subscriber = MailSubscriber(
            mail_to=["test@example.com"], mail_client=mock_mail_client
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
