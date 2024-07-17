from datetime import datetime

import pytest
from backend.application.item_management import add_item_to_inventory
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


@pytest.mark.django_db
class TestItem:
    def test_can_add_item_to_inventory(
        self, user: models.CustomUser, used_from: datetime, used_to: datetime
    ) -> None:
        user.save()
        user_id: int = user.pk

        item_dto: dtos.ItemDTO = dtos.ItemDTO(
            name="Test item",
            barcode="12345678",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user_id=user_id,
        )

        returned_item_dto: dtos.ItemDTO = add_item_to_inventory.add_item_to_inventory(
            item_dto
        )

        assert returned_item_dto.name == "Test item"
        assert returned_item_dto.barcode == "12345678"
        assert returned_item_dto.owner == "Owner"
        assert returned_item_dto.used_from == used_from
        assert returned_item_dto.used_to == used_to
        assert returned_item_dto.user_id == user_id
