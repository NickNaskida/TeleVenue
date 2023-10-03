from pydantic import BaseModel


class VenueItem(BaseModel):
    id: int
    name: str
    description: str
    address: str
    city: str
