import pytest
from backend.data import models
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def password_for_user() -> str:
    return "Password101!"


@pytest.fixture
def user(password_for_user: str) -> models.CustomUser:
    user = models.CustomUser(username="TestUser")
    user.set_password(password_for_user)
    user.save()
    return user


@pytest.mark.django_db
class TestTokenGeneration:
    def test_token_can_be_generated(
        self, password_for_user: str, user: models.CustomUser
    ) -> None:
        client = APIClient()

        response = client.post(
            "/api/auth_token/token",
            {
                "username": user.username,
                "password": password_for_user,
            },
        )

        # Check response/token
        assert response.status_code == 200
        token = response.data.get("token")
        assert token is not None

        # Check DB for token
        token_exists = Token.objects.filter(key=token).exists()
        assert token_exists

    def test_token_can_be_deleted(self, user: models.CustomUser):
        client = APIClient()

        # Create token
        token = Token.objects.create(user=user)

        # Check DB for token before deleting it
        user_token = Token.objects.filter(key=token)
        token_exists = user_token.exists()
        assert token_exists

        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = client.post("/api/auth_token/logout")

        # Check response
        assert response.status_code == 200

        # Check DB for token after deleting it
        token_exists = Token.objects.filter(key=token).exists()
        assert not token_exists
