from backend.domain.item_management import dtos, queries


def list_all_item_events_for_item(
    user_id: int, item_id: int
) -> list[dtos.GetItemEventDTO]:
    returned_item_events_list: list[dtos.GetItemEventDTO] = queries.get_item_events(
        user_id, item_id
    )
    return returned_item_events_list
