"""
routers/offers.py — Endpoints for browsing and searching job offers
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.offer import Offer
from app.schemas.offer import OfferResponse
from app.scraper.runner import run_all_scrapers

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