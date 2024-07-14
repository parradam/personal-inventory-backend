from datetime import datetime

import pytest
from backend.data import models
from django.utils import timezone


@pytest.fixture
def user() -> models.CustomUser:
    return models.CustomUser(username="TestUser", password="Password101!")


@pytest.fixture
def used_from() -> datetime:
    return timezone.make_aware(
        datetime(2020, 6, 30, 0, 0), timezone.get_default_timezone()
    )


@pytest.fixture
def used_to() -> datetime:
    return timezone.make_aware(
        datetime(2021, 12, 31, 0, 0), timezone.get_default_timezone()
    )


class TestItem:
    def test_can_create_item(
        self, user: models.CustomUser, used_from: datetime, used_to: datetime
    ) -> None:
        item: models.Item = models.Item(
            name="Test item",
            barcode="12345678",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user=user,
        )

        assert item.name == "Test item"
        assert item.barcode == "12345678"
        assert item.owner == "Owner"
        assert item.used_from == used_from
        assert item.used_to == used_to
        assert item.user == user
