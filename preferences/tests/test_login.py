from django.test import TestCase
from rest_framework import status
from ..models import UserData

class LoginViewTests(TestCase):
    def setUp(self):
        self.url = "/api/login/"
        self.user = UserData.objects.create(username="testuser", email="testuser@example.com", password="testpassword")
        self.valid_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        self.invalid_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }

    def test_login_valid_user(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_user(self):
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
