from backend.domain.item_management import dtos, queries


def get_one_item_for_user(user_id: int, item_id: int) -> dtos.ItemDTO:
    returned_items_list: dtos.ItemDTO = queries.get_item(user_id, item_id)
    return returned_items_list
