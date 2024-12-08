from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..models import UserData


class PrivacySettingsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.url = "/api/preferences/privacy_settings/"

    def test_get_privacy_settings_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("profile_visibility", response.data)

    def test_get_privacy_settings_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_privacy_settings_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        valid_data = {"profile_visibility": "private", "data_sharing": False}
        response = self.client.patch(self.url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile_visibility"], "private")
        self.assertFalse(response.data["data_sharing"])

    def test_update_privacy_settings_partial(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        partial_data = {"data_sharing": True}
        response = self.client.patch(self.url, partial_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data_sharing"])
