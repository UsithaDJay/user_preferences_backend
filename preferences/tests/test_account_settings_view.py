from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..models import UserData


class AccountSettingsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/preferences/account_settings/"
        self.user = UserData.objects.create(username="testuser", email="testuser@example.com", password="testpassword")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.valid_data = {
            "username": "newusername",
            "email": "newemail@example.com"
        }
        self.invalid_data = {
            "username": "",
            "email": "invalid-email"
        }

    def test_get_account_settings_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("username", response.data)

    def test_get_account_settings_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_account_settings_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.patch(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "newusername")

    def test_update_account_settings_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.patch(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
