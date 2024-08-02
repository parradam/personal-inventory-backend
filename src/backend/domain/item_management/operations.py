from backend.data import models
from backend.domain.item_management import dtos, mappers


def create_item(item_dto: dtos.ItemDTO) -> dtos.ItemDTO:
    user: models.CustomUser = models.CustomUser.objects.get(id=item_dto.user_id)

    item: models.Item = mappers.map_dto_to_model(item_dto, user)
    item.save()
    new_item_dto: dtos.ItemDTO = mappers.map_model_to_dto(item)

    return new_item_dto
