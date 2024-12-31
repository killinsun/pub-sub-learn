from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from loguru import logger

from app.dummy_mail_client import DummyMailClient
from app.subscribers import Subscriber, MailSubscriber

app = FastAPI()

subscribers: dict[str, list[Subscriber]] = {"new_article": []}


def get_mail_client() -> DummyMailClient:
    return DummyMailClient()


class Subscriber(BaseModel):
    email: EmailStr
    event_type: str


class Event(BaseModel):
    event_type: str
    data: dict


@app.post("/subscribe")
async def subscribe(
    subscriber: Subscriber, mail_client: DummyMailClient = Depends(get_mail_client)
):
    logger.info(f"Subscribing {subscriber.email} to {subscriber.event_type}")

    if subscriber.event_type not in subscribers:
        raise HTTPException(status_code=400, detail="Invalid event type")

    subscribers[subscriber.event_type].append(
        MailSubscriber(mail_client=mail_client, mail_to=[subscriber.email])
    )

    logger.info(
        f"Mail subscribers for {subscriber.event_type}: {len(subscribers[subscriber.event_type])}"
    )

    return {"email": subscriber.email, "event_type": subscriber.event_type}


@app.post("/publish")
async def publish(event: Event):
    logger.info(f"Publishing {event.event_type} event")
    logger.debug(event.data)
    logger.debug(subscribers)

    if event.event_type in subscribers:
        for subscriber in subscribers[event.event_type]:
            subscriber.notify(title="New article", message="Check out our new article!")
    else:
        logger.info("No subscribers for this event")

    return {"message": "Event published"}
