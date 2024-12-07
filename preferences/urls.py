from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    PreferencesView,
    AccountSettingsView,
    NotificationSettingsView,
    ThemeSettingsView,
    PrivacySettingsView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('preferences/', PreferencesView.as_view(), name='preferences'),
    path('preferences/account_settings/', AccountSettingsView.as_view(), name='account-settings'),
    path('preferences/notification_settings/', NotificationSettingsView.as_view(), name='notification-settings'),
    path('preferences/theme_settings/', ThemeSettingsView.as_view(), name='theme-settings'),
    path('preferences/privacy_settings/', PrivacySettingsView.as_view(), name='privacy-settings'),
]
