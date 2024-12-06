from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import AccountSettings, NotificationSettings, ThemeSettings, PrivacySettings
from .serializers import (
    UserSerializer,
    AccountSettingsSerializer,
    NotificationSettingsSerializer,
    ThemeSettingsSerializer,
    PrivacySettingsSerializer,
)

# User Registration View
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Account Settings API
class AccountSettingsView(generics.RetrieveUpdateAPIView):
    queryset = AccountSettings.objects.all()
    serializer_class = AccountSettingsSerializer
    permission_classes = [IsAuthenticated]


# Notification Settings API
class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer
    permission_classes = [IsAuthenticated]


# Theme Settings API
class ThemeSettingsView(generics.RetrieveUpdateAPIView):
    queryset = ThemeSettings.objects.all()
    serializer_class = ThemeSettingsSerializer
    permission_classes = [IsAuthenticated]


# Privacy Settings API
class PrivacySettingsView(generics.RetrieveUpdateAPIView):
    queryset = PrivacySettings.objects.all()
    serializer_class = PrivacySettingsSerializer
    permission_classes = [IsAuthenticated]
