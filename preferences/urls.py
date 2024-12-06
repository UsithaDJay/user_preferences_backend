from django.urls import path
from .views import (
    AccountSettingsView,
    NotificationSettingsView,
    ThemeSettingsView,
    PrivacySettingsView,
)

urlpatterns = [
    path('account-settings/<int:pk>/',
         AccountSettingsView.as_view(), name='account-settings'),
    path('notification-settings/<int:pk>/',
         NotificationSettingsView.as_view(), name='notification-settings'),
    path('theme-settings/<int:pk>/',
         ThemeSettingsView.as_view(), name='theme-settings'),
    path('privacy-settings/<int:pk>/',
         PrivacySettingsView.as_view(), name='privacy-settings'),
]
