from datetime import datetime

from attrs import define


@define
class ItemDTO:
    user_id: int
    name: str
    used_from: datetime
    used_to: datetime | None = None
    barcode: str | None = None
    owner: str | None = None
    id: int | None = None
