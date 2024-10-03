from datetime import datetime

import pytest
from backend.data import models
from backend.domain.item_management import dtos, queries
from django.utils import timezone


@pytest.fixture
def user() -> models.CustomUser:
    user = models.CustomUser(username="FirstUser", password="Password101!")
    user.save()
    return user


@pytest.fixture
def another_user() -> models.CustomUser:
    user = models.CustomUser(username="SecondUser", password="Password202!")
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
class TestGetListOfItems:
    def test_can_get_list_of_items(
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

        retrieved_items: list[dtos.ItemDTO] = queries.get_list_of_items(user_id=user.pk)

        # Check that correct list of items is returned
        assert len(retrieved_items) == 2

        # Assertions on item one
        assert retrieved_items[0].user_id == user.pk
        assert retrieved_items[0].name == item_one.name
        assert retrieved_items[0].barcode == item_one.barcode
        assert retrieved_items[0].owner == item_one.owner
        assert retrieved_items[0].used_from == item_one.used_from
        assert retrieved_items[0].used_to == item_one.used_to

        # Assertions on item two
        assert retrieved_items[1].user_id == user.pk
        assert retrieved_items[1].name == item_two.name
        assert retrieved_items[1].barcode == item_two.barcode
        assert retrieved_items[1].owner == item_two.owner
        assert retrieved_items[1].used_from == item_two.used_from
        assert retrieved_items[1].used_to == item_two.used_to

    def test_gets_only_users_items(
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
            user=another_user,
        )
        assert models.Item.objects.count() == 2

        retrieved_items: list[dtos.ItemDTO] = queries.get_list_of_items(user_id=user.pk)

        # Check that correct list of items is returned
        assert len(retrieved_items) == 1

        # Assertions on item one
        assert retrieved_items[0].user_id == user.pk
        assert retrieved_items[0].name == item_one.name
        assert retrieved_items[0].barcode == item_one.barcode
        assert retrieved_items[0].owner == item_one.owner
        assert retrieved_items[0].used_from == item_one.used_from
        assert retrieved_items[0].used_to == item_one.used_to

    def test_gets_list_of_items_no_items(
        self,
        user: models.CustomUser,
    ) -> None:
        # No items in DB
        assert models.Item.objects.count() == 0

        retrieved_items: list[dtos.ItemDTO] = queries.get_list_of_items(user_id=user.pk)

        # Check that correct list of items is returned
        assert len(retrieved_items) == 0


@pytest.mark.django_db
class TestGetItem:
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

        retrieved_item: dtos.ItemDTO = queries.get_item(
            user_id=user.pk, item_id=item_one.pk
        )

        # Assertions on item one
        assert retrieved_item.user_id == user.pk
        assert retrieved_item.name == item_one.name
        assert retrieved_item.barcode == item_one.barcode
        assert retrieved_item.owner == item_one.owner
        assert retrieved_item.used_from == item_one.used_from
        assert retrieved_item.used_to == item_one.used_to

    def test_does_not_get_other_users_items(
        self,
        user: models.CustomUser,
        another_user: models.CustomUser,
        used_from: datetime,
        used_to: datetime,
    ) -> None:
        # Create items in DB
        models.Item.objects.create(
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
            user=another_user,
        )
        assert models.Item.objects.count() == 2

        # This item doesn't belong to this user!
        with pytest.raises(models.Item.DoesNotExist):
            queries.get_item(user_id=user.pk, item_id=item_two.pk)

    def test_handles_no_items(
        self,
        user: models.CustomUser,
    ) -> None:
        # No items in DB
        assert models.Item.objects.count() == 0

        with pytest.raises(models.Item.DoesNotExist):
            queries.get_item(user_id=user.pk, item_id=1)


@pytest.mark.django_db
class TestGetItemEvents:
    def test_can_get_item_events(
        self, user: models.CustomUser, used_from: datetime, used_to: datetime
    ) -> None:
        # Create item in DB
        item_one: models.Item = models.Item.objects.create(
            name="Abacus",
            barcode="123",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user=user,
        )
        assert models.Item.objects.count() == 1

        # Create item event in DB
        models.ItemEvent.objects.create(
            item=item_one, description=f"{item_one.name} created."
        )
        assert models.ItemEvent.objects.count() == 1

        retrieved_item_events: list[dtos.GetItemEventDTO] = queries.get_item_events(
            user.pk, item_one.pk
        )

        # Assertions on item event
        assert len(retrieved_item_events) == 1
        assert retrieved_item_events[0].description == f"{item_one.name} created."
