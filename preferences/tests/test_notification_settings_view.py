from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..models import UserData

class NotificationSettingsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.url = "/api/preferences/notification_settings/"

    def test_get_notification_settings_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("frequency", response.data)

    def test_get_notification_settings_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_notification_settings_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        valid_data = {"frequency": "weekly", "email_notifications": False}
        response = self.client.patch(self.url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["frequency"], "weekly")
        self.assertFalse(response.data["email_notifications"])

    def test_update_notification_settings_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        invalid_data = {"frequency": "yearly"}  # Invalid choice
        response = self.client.patch(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
