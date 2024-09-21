from backend.data import models
from backend.domain.item_management import dtos


def map_model_to_dto(item_dto: models.Item) -> dtos.ItemDTO:
    return dtos.ItemDTO(
        user_id=item_dto.user.pk,
        name=item_dto.name,
        used_from=item_dto.used_from,
        used_to=item_dto.used_to,
        barcode=item_dto.barcode,
        owner=item_dto.owner,
        id=item_dto.pk,
    )


def map_model_to_update_item_dto(item_dto: models.Item) -> dtos.UpdateItemDTO:
    return dtos.UpdateItemDTO(
        user_id=item_dto.user.pk,
        name=item_dto.name,
        used_from=item_dto.used_from,
        used_to=item_dto.used_to,
        barcode=item_dto.barcode,
        owner=item_dto.owner,
        id=item_dto.pk,
    )


def map_dto_to_model(item_dto: dtos.ItemDTO, user: models.CustomUser) -> models.Item:
    return models.Item(
        user=user,
        name=item_dto.name,
        used_from=item_dto.used_from,
        used_to=item_dto.used_to,
        barcode=item_dto.barcode,
        owner=item_dto.owner,
        id=item_dto.id,
    )
