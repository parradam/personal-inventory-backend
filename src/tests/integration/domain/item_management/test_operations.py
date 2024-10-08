from datetime import datetime

import pytest
from backend.data import models
from backend.domain.item_management import dtos, mappers, operations
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
class TestCreateItem:
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

    def test_can_create_item_event(
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

        operations.create_item(item_dto)

        # First check that DB was updated
        returned_model: models.Item | None = models.Item.objects.first()
        assert returned_model is not None
        assert returned_model.name == "Test item"

        # Then check ItemEvent was created with message
        returned_item_event_model: models.ItemEvent | None = (
            models.ItemEvent.objects.first()
        )
        assert returned_item_event_model is not None
        assert returned_item_event_model.description == "Test item created."


@pytest.mark.django_db
class TestUpdateItem:
    def test_can_update_item(
        self,
        user: models.CustomUser,
        used_from: datetime,
        used_to: datetime,
        used_from_updated: datetime,
        used_to_updated: datetime,
    ) -> None:
        user.save()

        item_dto: dtos.ItemDTO = dtos.ItemDTO(
            name="Test item",
            barcode="12345678",
            owner="Owner",
            used_from=used_from,
            used_to=used_to,
            user_id=user.pk,
        )
        original_item_dto: dtos.ItemDTO = operations.create_item(item_dto)
        assert models.Item.objects.count() == 1
        assert original_item_dto.id

        update_item_dto: dtos.UpdateItemDTO = dtos.UpdateItemDTO(
            id=original_item_dto.id,
            name="Test item2",
            barcode="123456789",
            owner="Owner2",
            used_from=used_from_updated,
            used_to=used_to_updated,
            user_id=user.pk,
        )

        returned_item_dto = operations.update_item(update_item_dto, user.pk)

        assert returned_item_dto
        assert models.Item.objects.count() == 1

        # First check that DB was updated
        returned_model: models.Item | None = models.Item.objects.first()
        assert returned_model is not None
        assert returned_model.name == "Test item2"
        assert returned_model.barcode == "123456789"
        assert returned_model.owner == "Owner2"
        assert returned_model.used_from == used_from_updated
        assert returned_model.used_to == used_to_updated
        assert returned_model.user == user

        # Then check what was returned from domain layer
        assert returned_item_dto.name == "Test item2"
        assert returned_item_dto.barcode == "123456789"
        assert returned_item_dto.owner == "Owner2"
        assert returned_item_dto.used_from == used_from_updated
        assert returned_item_dto.used_to == used_to_updated
        assert returned_item_dto.user_id == user.pk


@pytest.mark.django_db
class TestDeleteItem:
    def test_can_delete_item(
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
        item: models.Item = mappers.map_dto_to_model(item_dto, user)
        item.save()

        assert models.Item.objects.count() == 1
        assert item.pk

        operations.delete_item(item.pk, user.pk)

        assert models.Item.objects.count() == 0
