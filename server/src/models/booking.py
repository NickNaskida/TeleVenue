from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import PkBase


class Booking(PkBase):
    """Booking model."""
    __tablename__ = 'bookings'

    venue_id = Column(String, ForeignKey('venues.id'))
    venue = relationship('Venue', lazy="selectin")
    user_id = Column(String)
    under_name = Column(String)
    date = Column(Date)
    comment = Column(String, nullable=True)
