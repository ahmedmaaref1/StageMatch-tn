"""
routers/offers.py — Endpoints for browsing and searching job offers
"""

from collections import Counter
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database import get_db
from app.models.offer import Offer
from app.schemas.offer import OfferResponse
from app.scraper.runner import run_all_scrapers
from app.scheduler import get_scheduler_status, run_scheduled_scraping

router = APIRouter(prefix="/offers", tags=["Offers"])


@router.get("", response_model=list[OfferResponse])
def get_offers(
    db: Session = Depends(get_db),
    domain: Optional[str] = Query(None, description="Filter by academic domain"),
    city: Optional[str] = Query(None, description="Filter by city"),
    search: Optional[str] = Query(None, description="Search keyword in title/company"),
    skip: int = Query(0, ge=0, description="Pagination skip offset"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
):
    """
    Returns a paginated list of offers with optional filters.
    """
    query = db.query(Offer)

    if domain:
        query = query.filter(Offer.domain == domain)

    if city:
        query = query.filter(Offer.city.ilike(f"%{city}%"))

    if search:
        search_filter = or_(
            Offer.title.ilike(f"%{search}%"),
            Offer.company.ilike(f"%{search}%"),
            Offer.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Order newest first
    offers = query.order_by(Offer.id.desc()).offset(skip).limit(limit).all()
    return offers


@router.get("/analytics")
def get_market_analytics(db: Session = Depends(get_db)):
    """
    Returns aggregated Tunisian tech job market statistics:
    - Total offers & unique companies
    - Breakdown by track / domain
    - Breakdown by city / region
    - Top 10 most demanded skills
    - Top hiring tech companies
    """
    total_offers = db.query(Offer).count()
    if total_offers == 0:
        return {
            "total_offers": 0,
            "total_companies": 0,
            "by_domain": [],
            "by_city": [],
            "top_skills": [],
            "top_companies": [],
            "top_track": "N/A",
            "top_skill": "N/A"
        }

    # 1. Total distinct tech companies
    total_companies = db.query(func.count(func.distinct(Offer.company))).scalar()

    # 2. Offers by tech track
    domain_counts = (
        db.query(Offer.domain, func.count(Offer.id))
        .group_by(Offer.domain)
        .order_by(func.count(Offer.id).desc())
        .all()
    )
    by_domain = [{"name": d[0], "count": d[1]} for d in domain_counts]
    top_track = by_domain[0]["name"] if by_domain else "N/A"

    # 3. Offers by city
    city_counts = (
        db.query(Offer.city, func.count(Offer.id))
        .group_by(Offer.city)
        .order_by(func.count(Offer.id).desc())
        .limit(6)
        .all()
    )
    by_city = [{"name": c[0], "count": c[1]} for c in city_counts]

    # 4. Top recruiting companies
    company_counts = (
        db.query(Offer.company, func.count(Offer.id))
        .group_by(Offer.company)
        .order_by(func.count(Offer.id).desc())
        .limit(8)
        .all()
    )
    top_companies = [{"name": c[0], "count": c[1]} for c in company_counts]

    # 5. Top 10 most demanded skills across all offers
    all_skills = []
    offers = db.query(Offer.skills).all()
    for o in offers:
        if o.skills and isinstance(o.skills, list):
            all_skills.extend(o.skills)

    skill_counter = Counter(all_skills)
    top_skills = [{"name": skill, "count": count} for skill, count in skill_counter.most_common(10)]
    top_skill = top_skills[0]["name"] if top_skills else "N/A"

    return {
        "total_offers": total_offers,
        "total_companies": total_companies,
        "by_domain": by_domain,
        "by_city": by_city,
        "top_skills": top_skills,
        "top_companies": top_companies,
        "top_track": top_track,
        "top_skill": top_skill
    }

@router.get("/scraping/status")
def get_cron_scraping_status():
    """
    Renvoie l'état du planificateur de scraping automatique (24h) :
    - is_active : True / False
    - last_run : date et heure de la dernière synchronisation
    - next_run : heure de la prochaine exécution planifiée (à 02h00)
    - last_inserted_count : nombre de nouveaux PFE ajoutés
    - last_status : 'Succès', 'En cours d'exécution...', etc.
    """
    return get_scheduler_status()


@router.post("/scraping/trigger")
def trigger_background_scraping(background_tasks: BackgroundTasks):
    """
    Permet de forcer un scraping immédiat sans attendre 02h00 du matin.
    Utilise BackgroundTasks pour exécuter la tâche en arrière-plan
    sans faire ramer ni bloquer l'utilisateur.
    """
    background_tasks.add_task(run_scheduled_scraping)
    return {
        "status": "triggered",
        "message": "Scraping d'arrière-plan démarré avec succès.",
        "scheduler": get_scheduler_status(),
    }


@router.get("/{offer_id}", response_model=OfferResponse)
def get_offer_by_id(offer_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single job offer by ID.
    """
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@router.post("/scrape")
def trigger_scrape(db: Session = Depends(get_db)):
    """
    Triggers our scraping pipeline and saves new offers directly into PostgreSQL!
    """
    raw_offers = run_all_scrapers(max_pages=1)
    inserted = 0

    for item in raw_offers:
        existing = db.query(Offer).filter(Offer.source_url == item["source_url"]).first()
        if not existing:
            new_offer = Offer(
                title=item.get("title", "Unknown"),
                company=item.get("company", "Entreprise"),
                city=item.get("city", "Tunisie"),
                domain=item.get("domain", "General"),
                contract_type=item.get("contract_type", "Stage PFE"),
                description=item.get("description", ""),
                skills=item.get("skills", []),
                source_url=item["source_url"],
                source_site=item.get("source_site", "scraper"),
                date_posted=item.get("date_posted"),
            )
            db.add(new_offer)
            inserted += 1

    db.commit()
    total = db.query(Offer).count()
    return {
        "status": "success",
        "scraped": len(raw_offers),
        "new_inserted": inserted,
        "total_in_db": total
    }