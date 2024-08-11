import io
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.application.item_management import add_item_to_inventory
from backend.domain.item_management import dtos
from backend.interfaces.item_management import serializers


class ItemList(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            stream = io.BytesIO(request.body)
            data: dict[str, Any] = JSONParser().parse(stream)
            data["user_id"] = request.user.pk
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        serializer: Any = serializers.Item(data=data)

        if serializer.is_valid():
            item_dto: dtos.ItemDTO = serializer.to_dto()
            returned_item_dto = add_item_to_inventory.add_item_to_inventory(item_dto)

            response_data: serializers.Item = serializers.Item(returned_item_dto)

            return JsonResponse(response_data.data, status=201, safe=False)
        return JsonResponse({"errors": serializer.errors}, status=400)
