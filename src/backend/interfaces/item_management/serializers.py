from typing import Any

from rest_framework import serializers

from backend.domain.item_management import dtos


class Item(serializers.Serializer[dtos.ItemDTO]):
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    used_from = serializers.DateTimeField()
    used_to = serializers.DateTimeField(default=None)
    barcode = serializers.CharField(max_length=50, default=None)
    owner = serializers.CharField(max_length=50, default=None)
    id = serializers.IntegerField(read_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["used_to"]:
            if attrs["used_from"] > attrs["used_to"]:
                raise serializers.ValidationError("Used to must be after used from.")
        return attrs

    def to_dto(self) -> dtos.ItemDTO:
        return dtos.ItemDTO(
            user_id=self.validated_data.get("user_id"),
            name=self.validated_data.get("name"),
            used_from=self.validated_data.get("used_from"),
            used_to=self.validated_data.get("used_to"),
            barcode=self.validated_data.get("barcode"),
            owner=self.validated_data.get("owner"),
            id=self.validated_data.get("id"),
        )
