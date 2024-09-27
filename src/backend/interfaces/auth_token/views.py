import datetime
from typing import Any

from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from rest_framework import status, views
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from backend.application.auth import register_user
from backend.interfaces.auth_token import serializers


class AuthCheckView(views.APIView):
    def get(self, request: Request) -> Response:
        cookie_params: dict[str, Any] = {
            "path": "/",
            "domain": None,
            "samesite": "None",
        }

        if hasattr(request, "invalid_cookie"):
            response = Response(
                {"authenticated": False}, status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie("auth_token", **cookie_params)
            return response

        if isinstance(request.user, AnonymousUser):
            response = Response(
                {"authenticated": False}, status=status.HTTP_401_UNAUTHORIZED
            )
            response.delete_cookie("auth_token", **cookie_params)
            return response

        return Response(
            {"authenticated": True},
            status=status.HTTP_200_OK,
        )


class RegisterView(views.APIView):
    def post(self, request: Request) -> Response:
        try:
            data = request.data
            serializer: serializers.RegisterUser = serializers.RegisterUser(data=data)

            if serializer.is_valid():
                username = serializer.validated_data.get("username")
                email = serializer.validated_data.get("email")
                password = serializer.validated_data.get("password")

                register_user.register_user(username, email, password)

                return Response(
                    {"username": username},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"errors": serializer.errors},  # type: ignore
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except IntegrityError:  # Unique constraint failed
            return Response(
                {"error": "A user with this username or email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(e)
            return Response(
                {"error": "There was an error signing you up. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(views.APIView):
    def post(self, request: Request) -> Response:
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                token, _created = Token.objects.get_or_create(user=user)

                expires: datetime.datetime = datetime.datetime.now(
                    datetime.UTC
                ) + datetime.timedelta(days=31)

                response = Response({"message": "Login successful"})
                response.set_cookie(
                    key="auth_token",
                    value=token.key,
                    httponly=True,
                    secure=True,
                    samesite="None",
                    expires=expires,
                    path="/",
                )

                return response
            else:
                return Response(
                    {"error": "Your username or password were incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                {"error": "There was an error signing you in. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["POST"])
def logout(request: Request) -> Response:
    user = request.user
    if user.is_authenticated:
        token = Token.objects.get(user=user)
        token.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
