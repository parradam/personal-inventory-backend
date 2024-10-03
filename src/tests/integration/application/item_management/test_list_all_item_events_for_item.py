from datetime import datetime

import pytest
from backend.application.item_management import list_all_item_events_for_item
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
class TestListAllItemEventsForItem:
    def test_can_list_all_item_events_for_item(
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

        retrieved_item_events: list[dtos.GetItemEventDTO] = (
            list_all_item_events_for_item.list_all_item_events_for_item(
                user.pk, item_one.pk
            )
        )

        # Assertions on item event
        assert len(retrieved_item_events) == 1
        assert retrieved_item_events[0].description == f"{item_one.name} created."
