from django.test import TestCase
from ninja.testing import TestClient

from conversations.api import router
from conversations.models import AIModel


"""Test suite for conversations API

Naming convention: test_{method_name}
Database: In-Memory SQLite
"""


TEST_USER_ID = "088948cc-e508-4ead-afde-7b9dd013a940"


class ConversationsTest(TestCase):
    databases = ['default']

    def test_create_converstaion(self):
        # Arrange
        payload = {
            "user_id": TEST_USER_ID,
            "configuration": {
                "temperature": 0.7,
                "model": AIModel.Name.GPT_4O
            }
        }
        # Act
        client = TestClient(router)
        response = client.post("/", json=payload)
        json = response.json()
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json["chat_id"])

    def test_list_configuration_options(self):
        # Act
        client = TestClient(router)
        response = client.post(":list_configuration_options")
        # Assert
        self.assertEqual(response.status_code, 200)
