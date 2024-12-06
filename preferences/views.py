from rest_framework import generics
from .models import AccountSettings, NotificationSettings, ThemeSettings, PrivacySettings
from .serializers import (
    AccountSettingsSerializer,
    NotificationSettingsSerializer,
    ThemeSettingsSerializer,
    PrivacySettingsSerializer,
)


class AccountSettingsView(generics.RetrieveUpdateAPIView):
    queryset = AccountSettings.objects.all()
    serializer_class = AccountSettingsSerializer


class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    queryset = NotificationSettings.objects.all()
    serializer_class = NotificationSettingsSerializer


class ThemeSettingsView(generics.RetrieveUpdateAPIView):
    queryset = ThemeSettings.objects.all()
    serializer_class = ThemeSettingsSerializer


class PrivacySettingsView(generics.RetrieveUpdateAPIView):
    queryset = PrivacySettings.objects.all()
    serializer_class = PrivacySettingsSerializer
