from datetime import datetime

import pytest
from backend.application.item_management.remove_item_from_inventory import (
    remove_item_from_inventory,
)
from backend.data import models
from django.utils import timezone


@pytest.fixture
def user() -> models.CustomUser:
    user = models.CustomUser(username="TestUser", password="Password101!")
    user.save()
    return user


@pytest.fixture
def another_user() -> models.CustomUser:
    user = models.CustomUser(username="AnotherTestUser", password="Password101!")
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
class TestListAllItemsForUser:
    def test_can_delete_item_for_user(
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
        item_two: models.Item = models.Item.objects.create(
            name="Beachball",
            barcode="456",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user=user,
        )
        assert models.Item.objects.count() == 2

        remove_item_from_inventory(item_one.pk, user.pk)

        # Check that correct list of items is returned
        assert models.Item.objects.count() == 1
        # Check that item_two is the only one left
        assert models.Item.objects.filter(pk=item_two.pk).exists()

    def test_cant_delete_item_for_another_user(
        self,
        user: models.CustomUser,
        another_user: models.CustomUser,
        used_from: datetime,
        used_to: datetime,
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

        remove_item_from_inventory(item_one.pk, another_user.pk)

        # Check that list of items is unchanged
        assert models.Item.objects.count() == 2
