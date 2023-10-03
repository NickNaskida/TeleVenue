from fastapi import APIRouter

from src.api.endpoints import venue
from src.api.endpoints import booking

api_router = APIRouter()

api_router.include_router(venue.router, prefix="/venues", tags=["venues"])
api_router.include_router(booking.router, prefix="/bookings", tags=["bookings"])
