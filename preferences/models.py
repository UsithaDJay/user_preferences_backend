from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.core.validators import MinLengthValidator


class UserData(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(4)])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20, validators=[MinLengthValidator(6)])

    def __str__(self):
        return self.username


class NotificationSettings(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    ON_DEMAND = 'on-demand'
    FREQUENCY_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (ON_DEMAND, 'On-demand'),
    ]

    user = models.OneToOneField(
        UserData, on_delete=models.CASCADE, related_name='notification_settings')
    frequency = models.CharField(
        max_length=50, choices=FREQUENCY_CHOICES, default=DAILY)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Notification Settings"


class ThemeSettings(models.Model):
    LIGHT = 'light'
    DARK = 'dark'
    THEME_CHOICES = [
        (LIGHT, 'Light'),
        (DARK, 'Dark'),
    ]

    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    FONT_SIZE_CHOICES = [
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
    ]

    user = models.OneToOneField(
        UserData, on_delete=models.CASCADE, related_name='theme_settings')
    theme = models.CharField(
        max_length=50, choices=THEME_CHOICES, default=LIGHT)
    font_size = models.CharField(
        max_length=10, choices=FONT_SIZE_CHOICES, default='medium')

    def __str__(self):
        return f"{self.user.username}'s Theme Settings"


class PrivacySettings(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROFILE_VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    user = models.OneToOneField(
        UserData, on_delete=models.CASCADE, related_name='privacy_settings')
    profile_visibility = models.CharField(
        max_length=50, choices=PROFILE_VISIBILITY_CHOICES, default=PUBLIC)
    data_sharing = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Privacy Settings"
    

@receiver(post_save, sender=UserData)
def create_user_preferences(sender, instance, created, **kwargs):
    if created:
        NotificationSettings.objects.create(user=instance)
        ThemeSettings.objects.create(user=instance)
        PrivacySettings.objects.create(user=instance)


@receiver(pre_delete, sender=UserData)
def delete_user_preferences(sender, instance, **kwargs):
    NotificationSettings.objects.filter(user=instance).delete()
    ThemeSettings.objects.filter(user=instance).delete()
    PrivacySettings.objects.filter(user=instance).delete()
