from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from loguru import logger

app = FastAPI()

subscribers: dict[str, list[EmailStr]] = {"new_article": []}


class Subscriber(BaseModel):
    email: EmailStr
    event_type: str


class Event(BaseModel):
    event_type: str
    data: dict


@app.post("/subscribe")
async def subscribe(subscriber: Subscriber):
    logger.info(f"Subscribing {subscriber.email} to {subscriber.event_type}")

    if subscriber.event_type not in subscribers:
        raise ValueError("Invalid event type")

    subscribers[subscriber.event_type].append(subscriber.email)

    return {"email": subscriber.email, "event_type": subscriber.event_type}


@app.post("/publish")
async def publish(event: Event):
    logger.info(f"Publishing {event.event_type} event")
    logger.debug(event.data)
    logger.debug(subscribers)

    if event.event_type in subscribers:
        for subscriber in subscribers[event.event_type]:
            logger.info(f"Sending email to {subscriber}")
    else:
        logger.info("No subscribers for this event")

    return {"message": "Event published"}
