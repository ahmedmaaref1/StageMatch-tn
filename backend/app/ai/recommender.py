import logging 
from typing import List,Dict,Any ,Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.models import Offer, Student

logger = logging.getLogger(__name__)

_MODEL = None 
MODEL_NAME = "all-MiniLM-L6-v2"  # Pre-trained model for sentence embeddings

def get_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        logger.info(f"Loading Sentence-Transformer model: {MODEL_NAME}")
        _MODEL = SentenceTransformer(MODEL_NAME)
        logger.info("Model loaded successfully.")
    return _MODEL   

def build_student_text(student: Student) -> str:
    skills_str = ", ".join(student.skills) if student.skills else "None specified"
    bio_str = student.bio if student.bio else ""

    text = (
        f"Domain: {student.domain}. "
        f"Degree Level: {student.degree_level} at {student.university}. "
        f"Preferred City: {student.preferred_city}. "
        f"Skills: {skills_str}. "
        f"Background and Objectives: {bio_str}"
    )
    return text.strip()

def build_offer_text(offer: Offer) -> str:
    skills_str = ", ".join(offer.skills) if offer.skills else ""
    desc_summary = offer.description[:500] if offer.description else ""
    text = (
        f"Job Title: {offer.title}. "
        f"Company: {offer.company}. "
        f"Domain: {offer.domain}. "
        f"Contract: {offer.contract_type}. "
        f"Location: {offer.city}. "
        f"Required Skills: {skills_str}. "
        f"Description: {desc_summary}"
    )
    return text.strip()

def calculate_skill_overlap(student_skills: List[str], offer_skills: List[str]) -> Tuple[List[str], float]:
    if not student_skills or not offer_skills:
        return [], 0.0
    student_set = {s.strip().lower() for s in student_skills if s}
    matching = []
    for skill in offer_skills:
        if skill.strip().lower() in student_set:
            matching.append(skill)
    # Overlap score = matching skills / total skills required by the job
    overlap_score = len(matching) / max(len(offer_skills), 1)
    return matching, min(overlap_score, 1.0)

def rank_offers_for_student(    student: Student,offers: List[Offer],top_k: int = 10) -> List[Dict[str, Any]]:
    if not student_skills or not offer_skills:
        return [], 0.0
    student_set = {s.strip().lower() for s in student_skills if s}
    matching = []
    for skill in offer_skills:
        if skill.strip().lower() in student_set:
            matching.append(skill)
    # Overlap score = matching skills / total skills required by the job
    overlap_score = len(matching) / max(len(offer_skills), 1)
    return matching, min(overlap_score, 1.0)

def rank_offers_for_student(
    student: Student,
    offers: List[Offer],
    top_k: int = 10
) -> List[Dict[str, Any]]:

    if not offers:
        return []
    model = get_model()
    # 1. Prepare text documents
    student_text = build_student_text(student)
    offer_texts = [build_offer_text(offer) for offer in offers]
    # 2. Compute 384-dimensional embeddings
    student_vector = model.encode([student_text], convert_to_numpy=True)
    offer_vectors = model.encode(offer_texts, convert_to_numpy=True)
    # 3. Compute Cosine Similarities (Shape: [1, N])
    similarities = cosine_similarity(student_vector, offer_vectors)[0]
    recommendations = []
        # 4. Compute composite score for each offer
    for idx, offer in enumerate(offers):
        semantic_sim = float(similarities[idx])
        # Normalize negative cosine similarities to 0
        semantic_sim = max(0.0, semantic_sim)

        # Skill overlap
        matching_skills, skill_score = calculate_skill_overlap(
            student.skills or [],
            offer.skills or []
        )

        # 1. Calculate Skill Gap (Missing skills required by this specific offer)
        offer_skills = offer.skills or []
        matching_lower = {s.lower() for s in matching_skills}
        missing_skills = [s for s in offer_skills if s.lower() not in matching_lower]

        # 2. Dynamic Career Advice & Match Explanation
        if not missing_skills:
            match_reason = "Profil parfait ! Vous validez 100% du stack technologique demandé."
        elif matching_skills:
            gap_hint = ", ".join(missing_skills[:2])
            match_reason = f"Vous validez {len(matching_skills)}/{len(offer_skills)} compétences clés. Acquérir {gap_hint} maximisera vos chances d'entretien."
        else:
            match_reason = "Match sémantique basé sur votre filière. Renforcez vos compétences pratiques sur ce stack."

        # Domain alignment bonus (+5% if domains match or if offer is general)
        domain_bonus = 0.0
        if offer.domain.lower() == student.domain.lower():
            domain_bonus = 0.05
        elif offer.domain.lower() == "general":
            domain_bonus = 0.02

        # Hybrid final score calculation
        composite_score = (semantic_sim * 0.70) + (skill_score * 0.30) + domain_bonus
        final_score = min(max(composite_score, 0.0), 1.0)
        match_percentage = int(round(final_score * 100))

        recommendations.append({
            "offer": offer,
            "match_score": match_percentage,
            "similarity_score": round(final_score, 4),
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "match_reason": match_reason,
            "semantic_score": round(semantic_sim * 100, 1),
            "skill_score": round(skill_score * 100, 1),
        })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:top_k]