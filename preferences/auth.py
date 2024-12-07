from .models import UserData
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

def get_token_from_request(request):
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        raise AuthenticationFailed("Authorization header is missing.")
    return authorization_header.split(' ')[1]

def authenticate(username, password):
    try:
        user = UserData.objects.get(username=username)
        if user.password == password:
            return user
    except UserData.DoesNotExist:
        return None
    return None

def get_user_from_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = UserData.objects.get(id=user_id)
        return user
    except Exception as e:
        raise AuthenticationFailed('Invalid token')