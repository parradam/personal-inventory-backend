import datetime

from django.contrib import auth
from rest_framework import status, views
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


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
        except Exception as e:
            print(e)
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
