from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.headers.get("Authorization")

        if not key:
            raise AuthenticationFailed("API key required")

        try:
            api_key = APIKey.objects.get(value=key, active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        return (api_key, None)