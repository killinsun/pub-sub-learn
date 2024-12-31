import abc
from typing import Optional

from pydantic import EmailStr


class Subscriber(abc.ABC):

    @abc.abstractmethod
    def get_event_type(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_subscriber_info(self) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    def notify(self, title: str, message: str):
        raise NotImplementedError


class MailSubscriber(Subscriber):
    def __init__(self, event_type: str, mail_to: list[EmailStr], mail_client):
        if len(mail_to) == 0:
            raise ValueError("mail_to cannot be empty")

        self.event_type = event_type
        self.mail_to = mail_to
        self.mail_client = mail_client

    def get_event_type(self) -> str:
        return self.event_type

    def get_subscriber_info(self) -> dict:
        return {
            "type": "mail",
            "email_to": self.mail_to,
        }

    def notify(self, title: str, message: str):
        self.mail_client.send_mail(
            mail_from="no-reply@example.com",
            mail_to=self.mail_to,
            subject=title,
            body=message,
        )
