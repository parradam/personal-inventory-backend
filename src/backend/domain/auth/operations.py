from backend.data import models


def create_user(username: str, email: str, password: str) -> None:
    user = models.CustomUser.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()
