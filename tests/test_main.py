from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestSubscribeRoot:

    def test_subscribe__adds_to_subscribers(self):
        response = client.post(
            "/subscribe",
            json={"email": "test@example.com", "event_type": "new_article"},
        )

        assert response.status_code == 200


class TestPublishRoot:

    def test_publish__notifies_subscribers(self):
        response = client.post(
            "/publish",
            json={
                "event_type": "new_article",
                "data": {"title": "Test", "body": "Test message"},
            },
        )

        assert response.status_code == 200
