import abc
import re

from loguru import logger


class NotificationInfrastructure(abc.ABC):
    @abc.abstractmethod
    def send(self, destination: str | list[str], title: str, content: str):
        raise NotImplementedError

    @abc.abstractmethod
    def validate_destination(self, destination: str | list[str]):
        raise NotImplementedError


class NullNotificationInfra(NotificationInfrastructure):
    """
    何もしない通知インフラストラクチャ
    """

    def send(self, destination: str | list[str], title: str, content: str):
        pass

    def validate_destination(self, destination: str | list[str]):
        pass


class MailNotificationInfra(NotificationInfrastructure):
    def send(self, destination: str | list[str], title: str, content: str):
        # 具体的なメール送信処理はここでは省略。
        logger.info(f"Sending email to {destination}")

    def validate_destination(self, destination: str | list[str]):
        if not isinstance(destination, list):
            destination = [destination]
        for email in destination:
            if not "@" in email:  # This is a simple check, not a full validation
                raise ValueError(f"Invalid email address: {email}")
