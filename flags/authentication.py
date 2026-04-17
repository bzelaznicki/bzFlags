from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class AdminKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        admin_key = request.headers.get("X-Admin-Key")

        if not admin_key:
            raise AuthenticationFailed("Missing admin key")

        if not secrets.compare_digest(admin_key, settings.ADMIN_SECRET_KEY):
            raise AuthenticationFailed("Invalid admin key")

        return (AnonymousUser(), admin_key)

    def authenticate_header(self, request):
        return "X-Admin-Key"
