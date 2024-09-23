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


class TestRegisterUser:
    @pytest.mark.django_db
    def test_user_can_be_registered(self) -> None:
        client = APIClient()

        response = client.post(
            "/api/auth_token/register",
            {
                "username": "new_user",
                "email": "new_user@test.com",
                "password": "password_for_user",
            },
        )

        # Check response
        assert response.status_code == 201
        assert response.data.get("username") == "new_user"

        # Check DB for user
        user_exists = models.CustomUser.objects.filter(username="new_user").exists()
        assert user_exists

    @pytest.mark.django_db
    def test_400_if_username_equals_password(self) -> None:
        client = APIClient()

        response = client.post(
            "/api/auth_token/register",
            {
                "username": "new_user",
                "email": "new_user@test.com",
                "password": "new_user",
            },
        )

        # Check response
        assert response.status_code == 400

        # Check DB for user
        user_exists = models.CustomUser.objects.filter(username="new_user").exists()
        assert not user_exists

    @pytest.mark.django_db
    def test_400_if_missing_username(self) -> None:
        client = APIClient()

        response = client.post(
            "/api/auth_token/register",
            {
                "email": "new_user@test.com",
                "password": "password_for_user",
            },
        )

        # Check response
        assert response.status_code == 400

        # Check DB for user
        user_exists = models.CustomUser.objects.filter(username="new_user").exists()
        assert not user_exists

    @pytest.mark.django_db
    def test_400_if_missing_email(self) -> None:
        client = APIClient()

        response = client.post(
            "/api/auth_token/register",
            {
                "username": "new_user",
                "password": "password_for_user",
            },
        )

        # Check response
        assert response.status_code == 400

        # Check DB for user
        user_exists = models.CustomUser.objects.filter(username="new_user").exists()
        assert not user_exists

    @pytest.mark.django_db
    def test_400_if_missing_password(self) -> None:
        client = APIClient()

        response = client.post(
            "/api/auth_token/register",
            {
                "username": "new_user",
                "email": "new_user@test.com",
            },
        )

        # Check response
        assert response.status_code == 400

        # Check DB for user
        user_exists = models.CustomUser.objects.filter(username="new_user").exists()
        assert not user_exists

    @pytest.mark.django_db(transaction=True)
    def test_400_if_user_exists(self) -> None:
        client = APIClient()

        first_response = client.post(
            "/api/auth_token/register",
            {
                "username": "new_user",
                "password": "password_for_user",
                "email": "new_user@test.com",
            },
        )

        # Check response
        assert first_response.status_code == 201

        second_response = client.post(
            "/api/auth_token/register",
            {
                "username": "new_user",
                "password": "password_for_user",
                "email": "new_user@test.com",
            },
        )

        # Check response
        assert second_response.status_code == 400

        # Check DB for user
        user_count = models.CustomUser.objects.filter(username="new_user").count()
        assert user_count == 1


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

    def test_token_can_be_deleted(self, user: models.CustomUser) -> None:
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
