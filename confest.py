import pytest
from django.conf import settings


@pytest.fixture(scope="session", autouse=True)
def print_database_info() -> None:
    """
    Fixture to print the current database information before running tests.
    """
    print(f"Using database: {settings.DATABASES['default']}")


@pytest.fixture(scope="session")
def django_db_setup() -> None:
    settings.DATABASES["test"]
