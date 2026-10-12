"""
seed_db.py — Loads scraped JSON offers into PostgreSQL
"""

import os
import sys
import json
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.offer import Offer


def seed_offers():
    # Find latest scraped JSON file in data/
    json_files = sorted(glob.glob("data/scraped_offers_*.json"))
    if not json_files:
        print("❌ No scraped JSON files found in data/. Run test_scraper.py first!")
        return

    latest_file = json_files[-1]
    print(f"📂 Reading latest data file: {latest_file}")

    with open(latest_file, "r", encoding="utf-8") as f:
        raw_offers = json.load(f)

    db = SessionLocal()
    inserted_count = 0
    skipped_count = 0

    try:
        for item in raw_offers:
            # Check if offer with this URL already exists to prevent duplicate inserts
            existing = db.query(Offer).filter(Offer.source_url == item["source_url"]).first()
            if existing:
                skipped_count += 1
                continue

            offer = Offer(
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
            db.add(offer)
            inserted_count += 1

        db.commit()
        print(f"🎉 Success! Inserted {inserted_count} new offers into PostgreSQL.")
        if skipped_count > 0:
            print(f"ℹ️  Skipped {skipped_count} duplicate offers.")

        total_in_db = db.query(Offer).count()
        print(f"📊 Total offers currently stored in PostgreSQL: {total_in_db}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting offers: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_offers()