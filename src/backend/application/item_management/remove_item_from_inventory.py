from backend.domain.item_management import operations


def remove_item_from_inventory(item_id: int, user_id: int) -> bool:
    has_item_been_removed: bool = operations.delete_item(item_id, user_id)
    return has_item_been_removed
