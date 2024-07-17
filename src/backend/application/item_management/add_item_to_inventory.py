from backend.domain.item_management import dtos, operations


def add_item_to_inventory(item_dto: dtos.ItemDTO) -> dtos.ItemDTO:
    returned_item_dto: dtos.ItemDTO = operations.create_item(item_dto)
    return returned_item_dto
