from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from loguru import logger

from app.dummy_mail_client import DummyMailClient
from app.infrastructure import MailNotificationInfra
from app.notification_service import NotificationService
from app.subscribers import MailSubscriber

app = FastAPI()


def get_mail_client() -> DummyMailClient:
    return DummyMailClient()


class EmailSubscribeRequest(BaseModel):
    email: EmailStr
    event_type: str


class Event(BaseModel):
    event_type: str
    data: dict


notification_service = NotificationService()
mail_infra = MailNotificationInfra()
notification_service.register_infrastructure(
    subscriber_type="MailSubscriber", infrastructure=mail_infra
)


@app.post("/subscribe")
async def subscribe(subscribe_req: EmailSubscribeRequest):
    logger.info(f"Subscribing {subscribe_req.email} to {subscribe_req.event_type}")

    mail_subscriber = MailSubscriber(
        event_type=subscribe_req.event_type, mail_to=[subscribe_req.email]
    )
    notification_service.add_subscriber(
        event_type=subscribe_req.event_type, subscriber=mail_subscriber
    )

    return {"email": subscribe_req.email, "event_type": subscribe_req.event_type}


@app.post("/publish")
async def publish(event: Event):
    logger.info(f"Publishing {event.event_type} event")
    logger.debug(event.data)

    notification_service.notify(
        title="New article published",
        message=f"New article published: {event.data}",
    )

    return {"message": "Event published"}
