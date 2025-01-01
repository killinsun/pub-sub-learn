import abc
from typing import Optional, Any

from pydantic import EmailStr
from loguru import logger

from app.infrastructure import NotificationInfrastructure


class Subscriber(abc.ABC):

    def __init__(self, destination: str | list[str] = None):
        self._infra: NotificationInfrastructure | None = None
        self.destination = destination

    @property
    def infra(self) -> NotificationInfrastructure:
        if self._infra is None:
            raise ValueError("NotificationInfrastructure is not set")

        return self._infra

    @infra.setter
    def infra(self, infra: NotificationInfrastructure):
        self._infra = infra
        logger.info(f"Setting infrastructure for {self.__class__.__name__}")

    @abc.abstractmethod
    def get_event_type(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_subscriber_info(self) -> dict:
        raise NotImplementedError

    def notify(self, destination: str | list[str], title: str, message: str):
        self.infra.send(destination=destination, title=title, content=message)

    def validate(self):
        self.infra.validate_destination(self.destination)


class MailSubscriber(Subscriber):
    def __init__(self, event_type: str, mail_to: list[EmailStr]):
        super().__init__(destination=mail_to)

        self.event_type = event_type
        self.mail_to = mail_to

    def get_event_type(self) -> str:
        return self.event_type

    def get_subscriber_info(self) -> dict:
        return {
            "type": "mail",
            "email_to": self.mail_to,
        }
