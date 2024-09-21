from typing import Any

from rest_framework import request
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request: request.Request) -> tuple[Any, Any] | None:
        # Check the 'Authorization' header first
        auth = super().authenticate(request)
        if auth:
            return auth

        # Fallback to checking the 'auth_token' cookie
        token = request.COOKIES.get("auth_token")
        if not token:
            return None

        try:
            return self.authenticate_credentials(token)
        except AuthenticationFailed:
            return None
