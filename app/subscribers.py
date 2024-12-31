import abc

from pydantic import EmailStr


class Subscriber(abc.ABC):
    @abc.abstractmethod
    def notify(self, title: str, message: str):
        raise NotImplementedError


class MailSubscriber(Subscriber):
    def __init__(self, mail_to: list[EmailStr], mail_client):
        if len(mail_to) == 0:
            raise ValueError("mail_to cannot be empty")

        self.mail_to = mail_to
        self.mail_client = mail_client

    def notify(self, title: str, message: str):

        self.mail_client.send_mail(
            mail_from="no-reply@example.com",
            mail_to=self.mail_to,
            subject=title,
            body=message,
        )
