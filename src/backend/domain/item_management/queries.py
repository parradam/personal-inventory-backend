from django.db.models import QuerySet

from backend.data import models
from backend.domain.item_management import dtos, mappers


def get_list_of_items(user_id: int) -> list[dtos.ItemDTO]:
    user: models.CustomUser = models.CustomUser.objects.get(id=user_id)
    items: QuerySet[models.Item] = user.item_set.all()

    item_dtos: list[dtos.ItemDTO] = list(map(mappers.map_model_to_dto, items))

    return item_dtos


def get_item(user_id: int, item_id: int) -> dtos.ItemDTO:
    item: models.Item = models.Item.objects.get(id=item_id, user__id=user_id)

    item_dto: dtos.ItemDTO = mappers.map_model_to_dto(item)

    return item_dto


def get_item_events(user_id: int, item_id: int) -> list[dtos.GetItemEventDTO]:
    item_events: QuerySet[models.ItemEvent] = models.ItemEvent.objects.filter(
        item_id=item_id, item__user_id=user_id
    )

    item_event_dtos: list[dtos.GetItemEventDTO] = list(
        map(mappers.map_item_event_model_to_dto, item_events)
    )

    return item_event_dtos
