from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from backend.data import models
from backend.domain.item_management import dtos, mappers


def create_item(item_dto: dtos.ItemDTO) -> dtos.ItemDTO:
    with transaction.atomic():
        user: models.CustomUser = models.CustomUser.objects.get(id=item_dto.user_id)

        item: models.Item = mappers.map_dto_to_model(item_dto, user)
        item.save()
        new_item_dto: dtos.ItemDTO = mappers.map_model_to_dto(item)

        event_description: str = f"{item.name} created."
        item_event: models.ItemEvent = models.ItemEvent(
            item=item, description=event_description
        )
        item_event.save()

        return new_item_dto


def update_item(item_dto: dtos.UpdateItemDTO, user_id: int) -> dtos.ItemDTO:
    item_to_update: models.Item = models.Item.objects.get(pk=item_dto.id)

    if item_to_update.user.pk == user_id:
        item_to_update.name = item_dto.name
        item_to_update.used_from = item_dto.used_from
        item_to_update.used_to = item_dto.used_to
        item_to_update.barcode = item_dto.barcode
        item_to_update.owner = item_dto.owner

        item_to_update.save()

    updated_item_dto = mappers.map_model_to_dto(item_to_update)
    return updated_item_dto


def delete_item(item_id: int, user_id: int) -> None:
    try:
        item_to_delete: models.Item = models.Item.objects.get(pk=item_id)
        # has_item_been_deleted = False
        if item_to_delete.user.pk == user_id:
            item_to_delete.delete()
            # has_item_been_deleted = number_of_items_deleted[0] == 1
        # return has_item_been_deleted
    except ObjectDoesNotExist:
        print(f"Item with ID {item_id} does not exist.")
    except Exception as e:
        print(f"Error deleting item with ID {item_id}: {e}")
