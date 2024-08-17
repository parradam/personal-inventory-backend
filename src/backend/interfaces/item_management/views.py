from typing import Any

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.application.item_management import (
    add_item_to_inventory,
    list_all_items_for_user,
)
from backend.domain.item_management import dtos
from backend.interfaces.item_management import serializers


class ItemList(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request: Request) -> Response:
        data = self.get_validated_data(request)
        if data is None:
            return Response({"error": "Invalid JSON"}, status=400)

        data["user_id"] = request.user.pk

        serializer: Any = serializers.Item(data=data)
        if serializer.is_valid():
            item_dto: dtos.ItemDTO = serializer.to_dto()
            returned_item_dto = add_item_to_inventory.add_item_to_inventory(item_dto)

            response_serializer: serializers.Item = serializers.Item(returned_item_dto)
            return Response(response_serializer.data, status=201)

        return Response({"errors": serializer.errors}, status=400)

    @permission_classes([IsAuthenticated])
    def get(self, request: Request) -> Response:
        try:
            user_id = request.user.pk
            returned_item_list: list[dtos.ItemDTO] = (
                list_all_items_for_user.list_all_items_for_user(user_id)
            )

            response_serializer: serializers.Item = serializers.Item(
                returned_item_list, many=True
            )
            return Response(response_serializer.data, status=200)
        except Exception:
            return Response(
                {"error": "There was an error retrieving the list of items"}, status=500
            )

    def get_validated_data(self, request: Request) -> dict[str, Any] | None:
        try:
            return request.data
        except Exception:
            return None
