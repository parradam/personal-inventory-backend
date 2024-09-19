from datetime import datetime

import pytest
from backend.application.item_management import (
    get_one_item_for_user,
)
from backend.data import models
from backend.domain.item_management import dtos
from django.utils import timezone


@pytest.fixture
def user() -> models.CustomUser:
    user = models.CustomUser(username="TestUser", password="Password101!")
    user.save()
    return user


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
class TestGetOneItemForUser:
    def test_can_get_item(
        self, user: models.CustomUser, used_from: datetime, used_to: datetime
    ) -> None:
        # Create items in DB
        item_one: models.Item = models.Item.objects.create(
            name="Abacus",
            barcode="123",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user=user,
        )
        models.Item.objects.create(
            name="Beachball",
            barcode="456",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user=user,
        )
        assert models.Item.objects.count() == 2

        returned_item: dtos.ItemDTO = get_one_item_for_user.get_one_item_for_user(
            item_one.user.pk, item_one.pk
        )

        # Assertions on item one
        assert returned_item.user_id == user.pk
        assert returned_item.name == item_one.name
        assert returned_item.barcode == item_one.barcode
        assert returned_item.owner == item_one.owner
        assert returned_item.used_from == item_one.used_from
        assert returned_item.used_to == item_one.used_to
