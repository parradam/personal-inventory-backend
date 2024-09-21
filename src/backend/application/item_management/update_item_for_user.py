from backend.domain.item_management import dtos, operations


def update_item_for_user(
    update_item_dto: dtos.UpdateItemDTO, user_id: int
) -> dtos.ItemDTO:
    updated_item_dto: dtos.ItemDTO = operations.update_item(update_item_dto, user_id)
    return updated_item_dto
