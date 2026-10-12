"""
schemas/offer.py — Pydantic validation schemas for Job Offers
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class OfferBase(BaseModel):
    title: str
    company: str
    city: str
    domain: str
    contract_type: str
    description: str
    skills: list[str] = []
    source_url: str
    source_site: str
    date_posted: Optional[str] = None


class OfferCreate(OfferBase):
    pass


class OfferResponse(OfferBase):
    id: int
    created_at: datetime

    # Tells Pydantic to read data directly from SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)