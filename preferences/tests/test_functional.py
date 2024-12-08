from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..models import UserData

class FunctionalTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"
        self.valid_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }

    def test_register_and_login(self):
        # Test registration
        register_response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", register_response.data)

        # Test login
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword"
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.data)

    def test_fetch_preferences(self):
        # Register a user and login
        self.client.post(self.register_url, self.valid_user_data)
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword"
        })
        token = login_response.data["token"]

        # Fetch preferences
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/preferences/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_update_account_settings(self):
        # Step 1: Register and login to get a token
        self.client.post(self.register_url, self.valid_user_data)
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword"
        })
        token = login_response.data["token"]
    
        # Step 2: Update account settings
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        update_response = self.client.patch("/api/preferences/account_settings/", {
            "username": "updateduser",
            "email": "updateduser@example.com"
        })
    
        # Step 3: Assertions
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["username"], "updateduser")
        self.assertEqual(update_response.data["email"], "updateduser@example.com")
    

    def test_update_notification_settings(self):
        # Register and login
        self.client.post(self.register_url, self.valid_user_data)
        login_response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword"
        })
        token = login_response.data["token"]

        # Update notification settings
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.patch("/api/preferences/notification_settings/", {
            "frequency": "weekly",
            "email_notifications": False
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["frequency"], "weekly")
        self.assertFalse(response.data["email_notifications"])

    def test_unauthenticated_access(self):
        response = self.client.get("/api/preferences/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
