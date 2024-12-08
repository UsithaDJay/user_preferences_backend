from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..models import UserData


class ThemeSettingsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.url = "/api/preferences/theme_settings/"

    def test_get_theme_settings_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("theme", response.data)

    def test_get_theme_settings_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_theme_settings_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        valid_data = {"theme": "dark", "font_size": "large"}
        response = self.client.patch(self.url, valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["theme"], "dark")
        self.assertEqual(response.data["font_size"], "large")

    def test_update_theme_settings_partial(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        partial_data = {"font_size": "small"}
        response = self.client.patch(self.url, partial_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["font_size"], "small")

