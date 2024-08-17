from datetime import datetime

import pytest
from backend.data import models
from backend.domain.item_management import dtos, operations
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
    def test_can_create_item(
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

        returned_item_dto: dtos.ItemDTO = operations.create_item(item_dto)

        # First check that DB was updated
        returned_model: models.Item | None = models.Item.objects.first()
        assert returned_model is not None
        assert returned_model.name == "Test item"
        assert returned_model.barcode == "12345678"
        assert returned_model.owner == "Owner"
        assert returned_model.used_from == used_from
        assert returned_model.used_to == used_to
        assert returned_model.user == user
        assert models.Item.objects.count() == 1

        # Then check what was returned from domain layer
        assert returned_item_dto.name == "Test item"
        assert returned_item_dto.barcode == "12345678"
        assert returned_item_dto.owner == "Owner"
        assert returned_item_dto.used_from == used_from
        assert returned_item_dto.used_to == used_to
        assert returned_item_dto.user_id == user_id
