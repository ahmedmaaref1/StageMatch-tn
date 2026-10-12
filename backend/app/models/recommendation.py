"""
models/recommendation.py — Association table caching AI match scores
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id", ondelete="CASCADE"), nullable=False)
    
    # Cosine similarity score calculated by sentence-transformers (0.0 to 1.0)
    similarity_score = Column(Float, nullable=False)
    # Overlapping skills between student and offer
    matching_skills = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships allow: rec.student and rec.offer
    student = relationship("Student", backref="recommendations")
    offer = relationship("Offer", backref="recommendations")

    def __repr__(self):
        return f"<Rec: Student {self.student_id} ──► Offer {self.offer_id} ({self.similarity_score:.2f})>"