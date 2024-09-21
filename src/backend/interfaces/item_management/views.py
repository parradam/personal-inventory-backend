from typing import Any, cast

from rest_framework import permissions, request, response, status, views

from backend.application.item_management import (
    add_item_to_inventory,
    get_one_item_for_user,
    list_all_items_for_user,
    remove_item_from_inventory,
    update_item_for_user,
)
from backend.domain.item_management import dtos
from backend.interfaces.item_management import serializers


class ItemList(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: request.Request) -> response.Response | None:
        try:
            data = request.data
            data["user_id"] = request.user.pk

            serializer: Any = serializers.Item(data=data)
            if serializer.is_valid():
                item_dto: dtos.ItemDTO = serializer.to_dto()
                returned_item_dto = add_item_to_inventory.add_item_to_inventory(
                    item_dto
                )

                response_serializer: serializers.Item = serializers.Item(
                    returned_item_dto
                )
                return response.Response(
                    response_serializer.data,  # type: ignore
                    status=status.HTTP_201_CREATED,
                )
            else:
                return response.Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception:
            return response.Response(
                {"error": "There was an error creating the item."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request: request.Request) -> response.Response:
        try:
            user_id: int = cast(int, request.user.pk)
            returned_item_list: list[dtos.ItemDTO] = (
                list_all_items_for_user.list_all_items_for_user(user_id)
            )

            response_serializer: serializers.Item = serializers.Item(
                returned_item_list,  # type: ignore
                many=True,
            )
            return response.Response(
                response_serializer.data,  # type: ignore
                status=status.HTTP_200_OK,
            )
        except Exception:
            return response.Response(
                {"detail": "There was an error retrieving the list of items."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ItemDetail(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: request.Request, pk: int) -> response.Response:
        try:
            item_id: int = pk
            user_id: int = cast(int, request.user.pk)

            returned_item = get_one_item_for_user.get_one_item_for_user(
                user_id, item_id
            )

            response_serializer: serializers.Item = serializers.Item(
                returned_item,
            )
            return response.Response(
                response_serializer.data,  # type: ignore
                status=status.HTTP_200_OK,
            )
        except Exception:
            return response.Response(
                {"error": "The item could not be retrieved."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request: request.Request, pk: int) -> response.Response:
        try:
            user_id: int = cast(int, request.user.pk)

            data = request.data
            data["user_id"] = user_id

            serializer: Any = serializers.UpdateItem(data=data)
            if serializer.is_valid():
                update_item_dto: dtos.UpdateItemDTO = serializer.to_dto()
                updated_item_dto = update_item_for_user.update_item_for_user(
                    update_item_dto, user_id
                )

                response_serializer: serializers.Item = serializers.Item(
                    updated_item_dto
                )
                return response.Response(
                    response_serializer.data,  # type: ignore
                    status=status.HTTP_200_OK,
                )
            else:
                return response.Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            print(e)
            return response.Response(
                {"error": "The item could not be retrieved."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request: request.Request, pk: int) -> response.Response:
        try:
            item_id: int = pk
            user_id: int = cast(int, request.user.pk)
            has_item_been_removed: bool = (
                remove_item_from_inventory.remove_item_from_inventory(item_id, user_id)
            )
            if has_item_been_removed:
                return response.Response(status=204)
            return response.Response(
                {"error": "The item could not be deleted"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception:
            return response.Response(
                {"error": "There was an error deleting the item"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
