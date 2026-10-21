"""
schemas/recommendation.py — Pydantic schema for recommendation responses
"""

from typing import List
from pydantic import BaseModel
from app.schemas.offer import OfferResponse


class RecommendationItem(BaseModel):
    match_score: int              # e.g. 85 (meaning 85%)
    similarity_score: float       # raw float e.g. 0.8524
    semantic_score: float         # pure AI semantic similarity percentage
    skill_score: float            # pure skill overlap percentage
    matching_skills: List[str]    # skills shared between student and offer
    missing_skills: List[str] = [] # skills required by the offer that the student lacks
    match_reason: str = ""        # personalized advisory insight
    offer: OfferResponse          # full job offer details


class StudentRecommendationsResponse(BaseModel):
    student_id: int
    student_name: str
    student_domain: str
    total_recommendations: int
    recommendations: List[RecommendationItem]