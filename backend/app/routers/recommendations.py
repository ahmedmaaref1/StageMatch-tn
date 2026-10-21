"""
routers/recommendations.py — API endpoint for AI-powered recommendations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.models.offer import Offer
from app.models.recommendation import Recommendation as DBRecommendation
from app.schemas.recommendation import StudentRecommendationsResponse, RecommendationItem
from app.ai.recommender import rank_offers_for_student

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{student_id}", response_model=StudentRecommendationsResponse)
def get_recommendations_for_student(
    student_id: int,
    top_k: int = Query(10, ge=1, le=50, description="Number of recommendations to return"),
    db: Session = Depends(get_db)
):
    """
    Computes AI semantic similarity and skill matching between
    the student profile and all available job offers in PostgreSQL.
    Caches the results in the recommendations table.
    """
    # 1. Fetch student
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # 2. Fetch all candidate offers
    offers = db.query(Offer).all()
    if not offers:
        raise HTTPException(status_code=404, detail="No job offers available in database")

    # 3. Run AI ranking engine
    ranked_results = rank_offers_for_student(student, offers, top_k=top_k)

    # 4. Optional: Cache top recommendations in the DB
    # Clear previous cached recommendations for this student
    db.query(DBRecommendation).filter(DBRecommendation.student_id == student.id).delete()

    for item in ranked_results:
        db_rec = DBRecommendation(
            student_id=student.id,
            offer_id=item["offer"].id,
            similarity_score=item["similarity_score"],
            matching_skills=item["matching_skills"]
        )
        db.add(db_rec)
    db.commit()

    # 5. Format response
    formatted_items = [
        RecommendationItem(
            match_score=r["match_score"],
            similarity_score=r["similarity_score"],
            semantic_score=r["semantic_score"],
            skill_score=r["skill_score"],
            matching_skills=r["matching_skills"],
            missing_skills=r.get("missing_skills", []),
            match_reason=r.get("match_reason", ""),
            offer=r["offer"]
        )
        for r in ranked_results
    ]

    return StudentRecommendationsResponse(
        student_id=student.id,
        student_name=student.full_name,
        student_domain=student.domain,
        total_recommendations=len(formatted_items),
        recommendations=formatted_items
    )