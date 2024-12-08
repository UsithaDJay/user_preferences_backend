from django.test import TestCase
from rest_framework import status
from ..models import UserData

class RegisterViewTests(TestCase):
    def setUp(self):
        self.url = "/api/register/"
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        self.invalid_data = {
            "username": "",
            "email": "invalid-email",
            "password": "short"
        }

    def test_register_valid_user(self):
        response = self.client.post(self.url, self.valid_data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertTrue(UserData.objects.filter(username="testuser").exists())

    def test_register_invalid_user(self):
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)  # Error messages for invalid fields
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        self.assertFalse(UserData.objects.filter(username="").exists())
        self.assertFalse(UserData.objects.filter(email="invalid-email").exists())
