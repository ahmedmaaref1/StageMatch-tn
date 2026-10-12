"""
runner.py — Orchestrates active Tunisian job scrapers
Active: TanitJobs, Tunisie Travail, LinkedIn
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from .tanitjobs import TanitJobsScraper
from .tunisie_travail import TunisieTravailScraper
from .linkedin import LinkedInScraper

logger = logging.getLogger(__name__)


def run_all_scrapers(max_pages: int = 1) -> list[dict]:
    """
    Runs our 3 working Tunisian scrapers.
    max_pages=1 gives ~47 offers.
    max_pages=2 gives ~90+ offers!
    """
    all_offers = []

    scrapers = [
        ("TanitJobs", TanitJobsScraper(delay_seconds=1.5)),
        ("Tunisie Travail", TunisieTravailScraper(delay_seconds=1.5)),
        ("LinkedIn", LinkedInScraper(delay_seconds=2.5)),
    ]

    for name, scraper in scrapers:
        logger.info(f"\n{'='*45}")
        logger.info(f"🕷️  Starting: {name}")
        logger.info(f"{'='*45}")
        try:
            offers = scraper.scrape(max_pages=max_pages)
            all_offers.extend([o.to_dict() for o in offers])
            logger.info(f"✅ {name}: {len(offers)} offers collected")
        except Exception as e:
            logger.error(f"❌ {name} scraper failed: {e}")

    logger.info(f"\n🎯 Total offers collected: {len(all_offers)}")
    return all_offers


def save_to_json(offers: list[dict], output_path: str = None) -> str:
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/scraped_offers_{timestamp}.json"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(offers, f, ensure_ascii=False, indent=2)

    logger.info(f"💾 Saved {len(offers)} offers to {output_path}")
    return output_path