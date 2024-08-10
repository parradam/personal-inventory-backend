from datetime import datetime

import pytest
from backend.application.item_management import list_all_items_for_user
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
class TestListAllItemsForUser:
    def test_can_list_items(
        self, user: models.CustomUser, used_from: datetime, used_to: datetime
    ) -> None:
        user.save()
        user_id: int = user.pk

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

        returned_item_list: list[dtos.ItemDTO] = (
            list_all_items_for_user.list_all_items_for_user(user_id)
        )

        # Check that correct list of items is returned
        assert len(returned_item_list) == 2

        # Assertions on item one
        assert returned_item_list[0].user_id == user.pk
        assert returned_item_list[0].name == item_one.name
        assert returned_item_list[0].barcode == item_one.barcode
        assert returned_item_list[0].owner == item_one.owner
        assert returned_item_list[0].used_from == item_one.used_from
        assert returned_item_list[0].used_to == item_one.used_to

        # Assertions on item two
        assert returned_item_list[1].user_id == user.pk
        assert returned_item_list[1].name == item_two.name
        assert returned_item_list[1].barcode == item_two.barcode
        assert returned_item_list[1].owner == item_two.owner
        assert returned_item_list[1].used_from == item_two.used_from
        assert returned_item_list[1].used_to == item_two.used_to
