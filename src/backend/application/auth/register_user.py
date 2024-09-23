from backend.domain.auth import operations


def register_user(username: str, email: str, password: str) -> None:
    operations.create_user(username, email, password)
