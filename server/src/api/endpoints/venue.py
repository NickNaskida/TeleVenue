from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from fastapi_async_sqlalchemy import db

from src.models.venue import Venue
from src.schemas.venue import VenueItem


router = APIRouter()


@router.get("/")
async def get_venues() -> List[VenueItem]:
    query = select(Venue)
    result = await db.session.execute(query)
    venues = result.scalars().all()
    return [
        VenueItem(
            id=row.id,
            name=row.name,
            description=row.description,
            address=row.address,
            city=row.city,
        ) for row in venues
    ]


@router.get("/{venue_id}")
async def get_venue_by_id(venue_id: int) -> VenueItem:
    query = select(Venue).where(Venue.id == venue_id)
    result = await db.session.execute(query)
    venue = result.scalars().first()
    return VenueItem(
        id=venue.id,
        name=venue.name,
        description=venue.description,
        address=venue.address,
        city=venue.city,
    )
