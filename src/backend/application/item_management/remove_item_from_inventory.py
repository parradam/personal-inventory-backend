from backend.domain.item_management import operations


def remove_item_from_inventory(item_id: int, user_id: int) -> None:
    operations.delete_item(item_id, user_id)
