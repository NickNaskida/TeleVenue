from datetime import date

from pydantic import BaseModel, ConfigDict

from src.schemas.venue import VenueItem


class BookingItem(BaseModel):
    id: int
    user_id: int
    under_name: str
    date: date
    comment: str
    venue: VenueItem

    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BaseModel):
    venue_id: int
    user_id: int
    under_name: str
    date: date
    comment: str
