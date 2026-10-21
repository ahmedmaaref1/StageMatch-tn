"""
tunisie_travail.py — Targeted Tech Scraper for tunisietravail.net
Searches specifically for 'stage informatique'.
"""

import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_tech_track, normalize_city

logger = logging.getLogger(__name__)


class TunisieTravailScraper(BaseScraper):
    BASE_URL = "https://www.tunisietravail.net"
    # Targeted IT search
    SEARCH_URL = "https://www.tunisietravail.net/page/{page}/?s=stage+informatique"

    def scrape(self, max_pages: int = 2) -> list[JobOffer]:
        all_offers = []
        for page_num in range(1, max_pages + 1):
            url = self.SEARCH_URL.format(page=page_num)
            html = self.fetch_page(url)
            if html is None:
                break

            offers = self.parse_listing_page(html)
            if not offers:
                break

            logger.info(f"Tunisie Travail Tech page {page_num}: {len(offers)} offers")
            all_offers.extend(offers)

        logger.info(f"Tunisie Travail total tech offers: {len(all_offers)}")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        offers = []

        articles = soup.find_all("article")
        if not articles:
            articles = soup.find_all("div", class_="post")

        for card in articles:
            try:
                offer = self._parse_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                logger.warning(f"Tunisie Travail card parse error: {e}")
                continue

        return offers

    def _parse_card(self, card) -> JobOffer | None:
        title_tag = card.find("h2") or card.find("h3")
        if not title_tag:
            return None

        link_tag = title_tag.find("a", href=True) or card.find("a", href=True)
        title = title_tag.get_text(strip=True)
        source_url = link_tag.get("href", self.BASE_URL) if link_tag else self.BASE_URL

        full_text = card.get_text(separator=" ", strip=True)
        date_tag = card.find("time") or card.find("span", class_="entry-date")
        date_posted = date_tag.get_text(strip=True) if date_tag else None

        skills = extract_skills_from_text(full_text)
        track = detect_tech_track(title, full_text)
        city = normalize_city(full_text)

        return JobOffer(
            title=title,
            company="Entreprise Tech Tunisie",
            city=city,
            description=full_text[:1000],
            skills=skills,
            source_url=source_url,
            source_site="tunisietravail",
            domain=track,
            date_posted=date_posted,
            contract_type="Stage PFE",
        )