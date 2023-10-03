from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import PkBase


class Booking(PkBase):
    """Booking model."""
    __tablename__ = 'bookings'

    venue_id = Column(String, ForeignKey('venues.id'))
    venue = relationship('Venue', lazy="selectin")
    user_id = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)




