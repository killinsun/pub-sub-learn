import json

from app.subscribers import Subscriber


def get_subscribers_dict(subscribers: list[Subscriber]) -> list[dict]:
    data = []
    for subscriber in subscribers:
        info = subscriber.get_subscriber_info()
        data.append(
            {
                "event_type": subscriber.get_event_type(),
                "notification": {
                    "type": info["type"],
                    "email_to": info["email_to"],
                },
            }
        )

    return data


class SubscribersRepository:
    def __init__(self, path: str):
        self.path = path

    def save_to_file(self, subscribers: dict[str, list[Subscriber]]):
        json_to_save = {"all_subscribers": []}
        with open(self.path, "w") as file:
            for event_type, subscribers_list in subscribers.items():
                json_to_save["all_subscribers"].append(
                    {
                        "event_type": event_type,
                        "subscribers": get_subscribers_dict(subscribers_list),
                    }
                )

            json.dump(json_to_save, file, indent=2)
