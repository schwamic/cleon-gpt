from django.test import TestCase
from ninja.testing import TestClient

from users.api import router


TEST_USER_ID = "088948cc-e508-4ead-afde-7b9dd013a940"


class UsersTest(TestCase):
    databases = ['default']

    def test_get_user(self):
        # Arrange
        user = {"id": TEST_USER_ID, "nickname": "Tester"}
        # Act
        client = TestClient(router)
        response = client.get(f"/{TEST_USER_ID}")
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), user)
