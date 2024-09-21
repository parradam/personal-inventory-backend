from datetime import datetime

import pytest
from backend.application.item_management import update_item_for_user
from backend.data import models
from backend.domain.item_management import dtos
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


@pytest.fixture
def used_from_updated() -> datetime:
    return timezone.make_aware(
        datetime(2018, 6, 30, 0, 0), timezone.get_default_timezone()
    )


@pytest.fixture
def used_to_updated() -> datetime:
    return timezone.make_aware(
        datetime(2019, 12, 31, 0, 0), timezone.get_default_timezone()
    )


@pytest.mark.django_db
class TestItem:
    def test_can_update_item_for_user(
        self,
        user: models.CustomUser,
        used_from: datetime,
        used_to: datetime,
        used_from_updated: datetime,
        used_to_updated: datetime,
    ) -> None:
        user.save()

        # Create items in DB
        item_one: models.Item = models.Item.objects.create(
            name="Abacus",
            barcode="123",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user=user,
        )

        item_dto_to_update: dtos.UpdateItemDTO = dtos.UpdateItemDTO(
            id=item_one.pk,
            name="Beachball",
            barcode="456",
            owner="New owner",
            used_from=used_from_updated,
            used_to=used_to_updated,
            user_id=user.pk,
        )

        updated_item_dto = update_item_for_user.update_item_for_user(
            item_dto_to_update, user.pk
        )

        assert updated_item_dto.name == "Beachball"
        assert updated_item_dto.barcode == "456"
        assert updated_item_dto.owner == "New owner"
        assert updated_item_dto.used_from == used_from_updated
        assert updated_item_dto.used_to == used_to_updated
        assert updated_item_dto.user_id == user.pk
