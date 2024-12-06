from django.contrib import admin
from .models import UserData, NotificationSettings, ThemeSettings, PrivacySettings

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'frequency', 'email_notifications', 'push_notifications')

@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'font_size')

@admin.register(PrivacySettings)
class PrivacySettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_visibility', 'data_sharing')
