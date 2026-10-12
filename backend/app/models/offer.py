"""
models/offer.py — Table for scraped job & internship offers
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False)
    city = Column(String(100), default="Tunisie", index=True)
    domain = Column(String(100), default="General", index=True)
    contract_type = Column(String(50), default="Stage PFE")
    description = Column(Text, nullable=False)
    # Stored as JSON array: ["Python", "FastAPI", "Docker"]
    skills = Column(JSON, default=list)
    # Unique constraint prevents duplicate offers when scraping again
    source_url = Column(String(500), unique=True, nullable=False)
    source_site = Column(String(50), nullable=False)
    date_posted = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Offer {self.id}: {self.title} @ {self.company} ({self.domain})>"