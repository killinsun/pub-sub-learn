import json
import tempfile

from app.subscribers import MailSubscriber
from app.subscribers_repository import SubscribersRepository


class TestSubscribersRepository:
    def test__restore_from_file__returns_subscribers(self):

        subscribers = {
            "new_article": [
                MailSubscriber(
                    mail_to=["test@example.com"],
                    mail_client=None,
                    event_type="new_article",
                ),
                MailSubscriber(
                    mail_to=["test2@example.com"],
                    mail_client=None,
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
