"""
test_ai.py — Quick test script for our AI Recommender Engine
"""

from app.database import SessionLocal
from app.models.student import Student
from app.models.offer import Offer
from app.ai.recommender import rank_offers_for_student

db = SessionLocal()

# 1. Fetch offers from PostgreSQL
offers = db.query(Offer).all()
print(f"📊 Loaded {len(offers)} offers from PostgreSQL database.")

# 2. Create a test student profile
mock_student = Student(
    full_name="Ahmed CS",
    email="ahmed.cs@test.tn",
    university="INSAT",
    degree_level="Licence 3",
    domain="Informatique & Développement",
    preferred_city="Tunis",
    skills=["Python", "FastAPI", "Docker", "SQL"],
    bio="Looking for a backend development PFE internship building REST APIs and web services."
)

print(f"\n👤 Testing recommendations for: {mock_student.full_name}")
print(f"   Domain: {mock_student.domain}")
print(f"   Skills: {mock_student.skills}")
print(f"   Bio: {mock_student.bio}\n")

# 3. Run AI ranking (Top 5 matches)
recs = rank_offers_for_student(mock_student, offers, top_k=5)

print("=" * 65)
print("🧠 TOP 5 AI RECOMMENDATIONS")
print("=" * 65)

for i, r in enumerate(recs, 1):
    offer = r["offer"]
    print(f"\n[{i}] {r['match_score']}% Match — {offer.title}")
    print(f"    🏢 Company          : {offer.company}")
    print(f"    📍 Location         : {offer.city}")
    print(f"    🎓 Domain           : {offer.domain}")
    print(f"    🤖 Semantic Sim     : {r['semantic_score']}%")
    print(f"    🎯 Skill Overlap    : {r['skill_score']}% (Matching: {r['matching_skills'] or 'None'})")

db.close()
print("\n✅ AI Recommendation Engine test complete!")