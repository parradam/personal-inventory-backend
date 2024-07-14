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


@pytest.mark.django_db
class TestItem:
    def test_can_create_and_retrieve_item(
        self, user: models.CustomUser, used_from: datetime, used_to: datetime
    ) -> None:
        user.save()

        item: models.Item = models.Item.objects.create(
            name="Test item",
            barcode="12345678",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user=user,
        )

        retrieved_item: models.Item = models.Item.objects.get(pk=item.pk)

        assert retrieved_item.name == "Test item"
        assert retrieved_item.barcode == "12345678"
        assert retrieved_item.owner == "Owner"
        assert retrieved_item.used_from == used_from
        assert retrieved_item.used_to == used_to
        assert retrieved_item.user == user
