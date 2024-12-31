from loguru import logger


class DummyMailClient:
    def send_mail(self, mail_from: str, mail_to: list[str], subject: str, body: str):
        logger.info(f"Sending email from {mail_from} to {mail_to}")
