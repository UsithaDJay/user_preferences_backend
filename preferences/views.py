from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from .models import UserData, NotificationSettings, ThemeSettings, PrivacySettings
from .serializers import (
    UserSerializer,
    LoginSerializer,
    NotificationSettingsSerializer,
    ThemeSettingsSerializer,
    PrivacySettingsSerializer,
)
from .auth import authenticate, get_user_from_token

# User Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="Login an existing user",
        request_body=LoginSerializer,  # Use the new serializer here
        responses={
            200: "Login successful, tokens returned",
            401: "Invalid credentials",
        },
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
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
        token = request.headers.get('Authorization').split(' ')[1]
        user = get_user_from_token(token)
        try:
            user_data = UserData.objects.get(id=user.id)
            notification_settings = NotificationSettings.objects.get(user_id=user.id)
            theme_settings = ThemeSettings.objects.get(user_id=user.id)
            privacy_settings = PrivacySettings.objects.get(user_id=user.id)
            
            data = {
                'user_data': UserSerializer(user_data).data,
                'notification_settings': NotificationSettingsSerializer(notification_settings).data,
                'theme_settings': ThemeSettingsSerializer(theme_settings).data,
                'privacy_settings': PrivacySettingsSerializer(privacy_settings).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except (UserData.DoesNotExist, NotificationSettings.DoesNotExist, ThemeSettings.DoesNotExist, PrivacySettings.DoesNotExist):
            return Response({"error": "Preferences not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdatePreferencesView(APIView):
    @transaction.atomic
    def patch(self, request, section):
        token = request.headers.get('Authorization').split(' ')[1]
        user = get_user_from_token(token)
        data = request.data
        
        try:
            if section == 'account_settings':
                instance = UserData.objects.get(id=user.id)
                serializer = UserSerializer(instance, data=data, partial=True)
            elif section == 'notification_settings':
                instance = NotificationSettings.objects.get(user_id=user.id)
                serializer = NotificationSettingsSerializer(instance, data=data, partial=True)
            elif section == 'theme_settings':
                instance = ThemeSettings.objects.get(user_id=user.id)
                serializer = ThemeSettingsSerializer(instance, data=data, partial=True)
            elif section == 'privacy_settings':
                instance = PrivacySettings.objects.get(user_id=user.id)
                serializer = PrivacySettingsSerializer(instance, data=data, partial=True)
            else:
                return Response({'detail': 'Invalid section'}, status=status.HTTP_400_BAD_REQUEST)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            transaction.set_rollback(True)
            return Response({"error": f"{section.replace('_', ' ').title()} not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
