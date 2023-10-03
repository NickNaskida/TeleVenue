from sqlalchemy import Column, String

from src.models.base import PkBase


class Venue(PkBase):
    """Venues model."""
    __tablename__ = 'venues'

    name = Column(String(255), nullable=False)
    description = Column(String(600), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)



