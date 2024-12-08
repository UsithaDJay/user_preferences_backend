from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserSerializer,
    LoginSerializer,
    NotificationSettingsSerializer,
    ThemeSettingsSerializer,
    PrivacySettingsSerializer,
)
from .auth import get_token_from_request, authenticate, get_user_from_token

# User Registration View
class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=UserSerializer,
        responses={201: "User registered successfully", 400: "Invalid input"},
    ) 

    @transaction.atomic
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'token': str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    # permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Login an existing user",
        request_body=LoginSerializer,  # Use the new serializer here
        responses={
            200: "Login successful, tokens returned",
            401: "Invalid credentials",
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'token': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class PreferencesView(APIView):
    def get(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            preferences = [
                {"section": "account_settings", "name": "Account Settings"},
                {"section": "notification_settings", "name": "Notification Settings"},
                {"section": "theme_settings", "name": "Theme Settings"},
                {"section": "privacy_settings", "name": "Privacy Settings"},
            ]
            return Response(preferences, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AccountSettingsView(APIView):
    """
    Handles fetching and updating account settings.
    """
    def get(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def patch(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            transaction.set_rollback(True)
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class NotificationSettingsView(APIView):
    """
    Handles fetching and updating notification settings.
    """
    def get(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            notification_settings = user.notification_settings
            serializer = NotificationSettingsSerializer(notification_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def patch(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            notification_settings = user.notification_settings
            serializer = NotificationSettingsSerializer(notification_settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            transaction.set_rollback(True)
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ThemeSettingsView(APIView):
    """
    Handles fetching and updating theme settings.
    """
    def get(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            theme_settings = user.theme_settings
            serializer = ThemeSettingsSerializer(theme_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def patch(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            theme_settings = user.theme_settings
            serializer = ThemeSettingsSerializer(theme_settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            transaction.set_rollback(True)
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PrivacySettingsView(APIView):
    def get(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            privacy_settings = user.privacy_settings
            serializer = PrivacySettingsSerializer(privacy_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def patch(self, request):
        try:
            token = get_token_from_request(request)
            user = get_user_from_token(token)
            privacy_settings = user.privacy_settings
            serializer = PrivacySettingsSerializer(privacy_settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            transaction.set_rollback(True)
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
