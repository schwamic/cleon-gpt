from django.test import TestCase
from ninja.testing import TestClient

from conversations.api import router


TEST_USER_ID = "088948cc-e508-4ead-afde-7b9dd013a940"


class ConversationsTest(TestCase):
    databases = ['default']

    def test_create_converstaion(self):
        # Arrange
        payload = {
            "user_id": TEST_USER_ID,
            "configuration": {
                "temperature": 0.7
            },
            "model": "GPT-4o"
        }
        # Act
        client = TestClient(router)
        response = client.post("/", json=payload)
        json = response.json()
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json["chat_id"])
