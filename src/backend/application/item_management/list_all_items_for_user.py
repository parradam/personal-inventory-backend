from backend.domain.item_management import dtos, queries


def list_all_items_for_user(user_id: int) -> list[dtos.ItemDTO]:
    returned_items_list: list[dtos.ItemDTO] = queries.get_list_of_items(user_id)
    return returned_items_list
