import pytest

from app.infrastructure import MailNotificationInfra


class TestMailNotificationInfra:

    def test_validate_destination__accepts_single_email(self):
        infra = MailNotificationInfra()
        assert infra.validate_destination("test@example.com") is None

    def test_validate_destination__accepts_list_of_emails(self):
        infra = MailNotificationInfra()
        assert (
            infra.validate_destination(["test1@example.com", "test2@example.com"])
            is None
        )

    def test_validate_destination__raises_error(self):
        infra = MailNotificationInfra()
        with pytest.raises(ValueError):
            infra.validate_destination("hoge")
            infra.validate_destination(["hoge", "fuga"])
