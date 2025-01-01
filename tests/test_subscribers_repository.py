import json
import tempfile

from app.subscribers import MailSubscriber
from app.subscribers_repository import SubscribersRepository, get_subscribers_dict


class TestSubscribersRepository:
    def test__restore_from_file__returns_subscribers(self):

        subscribers = {
            "new_article": [
                MailSubscriber(
                    mail_to=["test@example.com"],
                    event_type="new_article",
                ),
                MailSubscriber(
                    mail_to=["test2@example.com"],
                    event_type="new_article",
                ),
            ],
        }

        temp_file_path = tempfile.NamedTemporaryFile().name

        repo = SubscribersRepository(path=temp_file_path)
        repo.save_to_file(subscribers)

        file = open(temp_file_path, "r")
        data = file.read()

        data_dict = json.loads(data)

        assert data_dict == {
            "all_subscribers": [
                {
                    "event_type": "new_article",
                    "subscribers": [
                        {
                            "event_type": "new_article",
                            "notification": {
                                "type": "mail",
                                "email_to": ["test@example.com"],
                            },
                        },
                        {
                            "event_type": "new_article",
                            "notification": {
                                "type": "mail",
                                "email_to": ["test2@example.com"],
                            },
                        },
                    ],
                },
            ],
        }

    def test_restore_from_file__returns_subscribers(self):
        subscribers = {
            "new_article": [
                MailSubscriber(
                    mail_to=["test@example.com"],
                    event_type="new_article",
                ),
                MailSubscriber(
                    mail_to=["test2@example.com"],
                    event_type="new_article",
                ),
            ],
        }

        temp_file_path = tempfile.NamedTemporaryFile().name

        json_to_save = {"all_subscribers": []}
        with open(temp_file_path, "w") as file:
            for event_type, subscribers_list in subscribers.items():
                json_to_save["all_subscribers"].append(
                    {
                        "event_type": event_type,
                        "subscribers": get_subscribers_dict(subscribers_list),
                    }
                )

            json.dump(json_to_save, file, indent=2)

        repo = SubscribersRepository(path=temp_file_path)
        subscribers = repo.restore_from_file()

        assert len(subscribers["new_article"]) == 2
        assert subscribers["new_article"][0].mail_to == ["test@example.com"]
        assert subscribers["new_article"][1].mail_to == ["test2@example.com"]
