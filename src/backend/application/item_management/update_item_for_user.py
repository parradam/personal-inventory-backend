from backend.domain.item_management import dtos, operations


def update_item_for_user(
    item_dto: dtos.UpdateItemDTO, user_id: int
) -> dtos.UpdateItemDTO:
    updated_item_dto: dtos.UpdateItemDTO = operations.update_item(item_dto, user_id)
    return updated_item_dto
