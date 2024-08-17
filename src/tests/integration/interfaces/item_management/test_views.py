from datetime import datetime
from datetime import timezone as tz

import pytest
from backend.data import models
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def password_for_user() -> str:
    return "Password101!"


@pytest.fixture
def user(password_for_user: str) -> models.CustomUser:
    user = models.CustomUser(username="TestUser")
    user.set_password(password_for_user)
    user.save()
    return user


@pytest.fixture
def used_from() -> str:
    dt = timezone.make_aware(datetime(2024, 8, 1, 12, 34, 56), tz.utc)
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


@pytest.fixture
def used_to() -> str:
    dt = timezone.make_aware(datetime(2020, 8, 1, 12, 34, 56), tz.utc)
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


@pytest.fixture
def valid_item(used_from: str) -> dict[str, str | int]:
    item: dict[str, str | int] = {
        "name": "An item",
        "barcode": "123456",
        "owner": "Adam",
        "used_from": used_from,
    }
    return item


@pytest.fixture
def item_without_name(used_from: str) -> dict[str, str | int]:
    item: dict[str, str | int] = {
        "barcode": "123456",
        "owner": "Adam",
        "used_from": used_from,
    }
    return item


@pytest.fixture
def item_with_invalid_used_dates(used_from: str, used_to: str) -> dict[str, str | int]:
    item: dict[str, str | int] = {
        "name": "An item",
        "barcode": "123456",
        "owner": "Adam",
        "used_from": used_from,
        "used_to": used_to,
    }
    return item


@pytest.mark.django_db
class TestItemListPost:
    def test_item_can_be_created(
        self, user: models.CustomUser, valid_item: dict[str, str | int]
    ) -> None:
        client = APIClient()

        # Create token for user
        token = Token.objects.create(user=user)

        # Create item
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = client.post(
            "/api/item_management/items/", data=valid_item, format="json"
        )

        # Check response
        assert response.status_code == 201

        # Check content
        returned_item = response.json()
        assert returned_item is not None
        assert returned_item["name"] == valid_item["name"]
        assert returned_item["barcode"] == valid_item["barcode"]
        assert returned_item["owner"] == valid_item["owner"]
        assert returned_item["used_from"] == valid_item["used_from"]

        # Check DB for item
        items_in_db = models.Item.objects.filter(name=valid_item["name"])
        assert items_in_db.count() == 1
        assert items_in_db[0].name == valid_item["name"]
        assert items_in_db[0].barcode == valid_item["barcode"]
        assert items_in_db[0].owner == valid_item["owner"]

        used_from_iso = datetime.fromisoformat(str(valid_item["used_from"]))
        assert items_in_db[0].used_from == used_from_iso

    def test_item_not_created_when_not_logged_in(
        self, valid_item: dict[str, str | int]
    ) -> None:
        client = APIClient()

        # Atempt to create item
        response = client.post(
            "/api/item_management/items/", data=valid_item, format="json"
        )

        assert response.status_code == 400

    def test_item_not_created_without_name(
        self, user: models.CustomUser, item_without_name: dict[str, str | int]
    ) -> None:
        client = APIClient()

        # Create token for user
        token = Token.objects.create(user=user)

        # Attempt to create item
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = client.post(
            "/api/item_management/items/", data=item_without_name, format="json"
        )

        # Check response
        assert response.status_code == 400

        # Check DB for item
        items_in_db = models.Item.objects.all()
        assert items_in_db.count() == 0

    def test_item_not_created_with_used_to_before_used_from(
        self,
        user: models.CustomUser,
        item_with_invalid_used_dates: dict[str, str | int],
    ) -> None:
        client = APIClient()

        # Create token for user
        token = Token.objects.create(user=user)

        # Attempt to create item
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = client.post(
            "/api/item_management/items/",
            data=item_with_invalid_used_dates,
            format="json",
        )

        # Check response
        assert response.status_code == 400

        # Check DB for item
        items_in_db = models.Item.objects.all()
        assert items_in_db.count() == 0


@pytest.mark.django_db
class TestItemListGet:
    def test_empty_item_list_can_be_retrieved(self, user: models.CustomUser) -> None:
        client = APIClient()

        # Create token for user
        token = Token.objects.create(user=user)

        # Get item list
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = client.get("/api/item_management/items/")

        # Check response
        assert response.status_code == 200

        # # Check content
        returned_items = response.json()
        assert returned_items is not None
        assert len(returned_items) == 0

    def test_item_list_can_be_retrieved(
        self, user: models.CustomUser, used_from: datetime, used_to: datetime
    ) -> None:
        client = APIClient()

        # Create token for user
        token = Token.objects.create(user=user)

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

        # Get item list
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = client.get("/api/item_management/items/")

        # Check response
        assert response.status_code == 200

        # # Check content
        returned_item_list = response.json()
        assert returned_item_list is not None
        assert len(returned_item_list) == 2

        # Assertions on item one
        assert returned_item_list[0]["user_id"] == user.pk
        assert returned_item_list[0]["name"] == item_one.name
        assert returned_item_list[0]["barcode"] == item_one.barcode
        assert returned_item_list[0]["owner"] == item_one.owner
        assert returned_item_list[0]["used_from"] == item_one.used_from
        assert returned_item_list[0]["used_to"] == item_one.used_to

        # Assertions on item two
        assert returned_item_list[1]["user_id"] == user.pk
        assert returned_item_list[1]["name"] == item_two.name
        assert returned_item_list[1]["barcode"] == item_two.barcode
        assert returned_item_list[1]["owner"] == item_two.owner
        assert returned_item_list[1]["used_from"] == item_two.used_from
        assert returned_item_list[1]["used_to"] == item_two.used_to
