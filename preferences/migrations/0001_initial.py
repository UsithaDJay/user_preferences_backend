# Generated by Django 5.1.4 on 2024-12-06 20:44

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserData",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "username",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        validators=[django.core.validators.MinLengthValidator(4)],
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "password",
                    models.CharField(
                        max_length=20,
                        validators=[django.core.validators.MinLengthValidator(6)],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ThemeSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "theme",
                    models.CharField(
                        choices=[("light", "Light"), ("dark", "Dark")],
                        default="light",
                        max_length=50,
                    ),
                ),
                (
                    "font_size",
                    models.CharField(
                        choices=[
                            ("small", "Small"),
                            ("medium", "Medium"),
                            ("large", "Large"),
                        ],
                        default="medium",
                        max_length=10,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="theme_settings",
                        to="preferences.userdata",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PrivacySettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_visibility",
                    models.CharField(
                        choices=[("public", "Public"), ("private", "Private")],
                        default="public",
                        max_length=50,
                    ),
                ),
                ("data_sharing", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="privacy_settings",
                        to="preferences.userdata",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NotificationSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("daily", "Daily"),
                            ("weekly", "Weekly"),
                            ("monthly", "Monthly"),
                            ("on-demand", "On-demand"),
                        ],
                        default="daily",
                        max_length=50,
                    ),
                ),
                ("email_notifications", models.BooleanField(default=True)),
                ("push_notifications", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification_settings",
                        to="preferences.userdata",
                    ),
                ),
            ],
        ),
    ]
