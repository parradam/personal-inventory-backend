from typing import Any

from rest_framework import serializers

from backend.domain.auth import dtos


class RegisterUser(serializers.Serializer[dtos.RegisterUserDTO]):
    username = serializers.CharField(min_length=6, max_length=20)
    email = serializers.EmailField(min_length=6, max_length=30)
    password = serializers.CharField(min_length=6, max_length=20)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["username"] == attrs["password"]:
            raise serializers.ValidationError(
                {"password": "Password must be different from username."}
            )
        return attrs
