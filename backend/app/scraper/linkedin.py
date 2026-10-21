"""
linkedin.py — Targeted Tech Scraper for LinkedIn Jobs in Tunisia
Searches specifically for 'stage pfe informatique'.
"""

import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_tech_track, normalize_city

logger = logging.getLogger(__name__)


class LinkedInScraper(BaseScraper):
    BASE_URL = "https://www.linkedin.com"
    # Targeted tech query on LinkedIn guest endpoint
    SEARCH_URL = (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        "?keywords=stage%20pfe%20informatique&location=Tunisia&start={start}"
    )

    def __init__(self, delay_seconds: float = 2.5):
        super().__init__(delay_seconds=delay_seconds)

    def scrape(self, max_pages: int = 2) -> list[JobOffer]:
        all_offers = []
        for page_num in range(max_pages):
            start_offset = page_num * 25
            url = self.SEARCH_URL.format(start=start_offset)
            html = self.fetch_page(url)

            if html is None:
                break

            offers = self.parse_listing_page(html)
            if not offers:
                break

            logger.info(f"LinkedIn Tech page {page_num + 1}: {len(offers)} offers")
            all_offers.extend(offers)

        logger.info(f"LinkedIn total tech offers: {len(all_offers)}")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        offers = []

        cards = soup.find_all("li")
        if not cards:
            cards = soup.find_all("div", class_="base-card")

        for card in cards:
            try:
                offer = self._parse_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                continue

        return offers

    def _parse_card(self, card) -> JobOffer | None:
        title_tag = card.find("h3", class_="base-search-card__title") or card.find("h3")
        if not title_tag:
            return None
        title = title_tag.get_text(strip=True)

        company_tag = card.find("h4", class_="base-search-card__subtitle") or card.find("a", class_="hidden-nested-link")
        company = company_tag.get_text(strip=True) if company_tag else "Entreprise Tech Tunisie"

        location_tag = card.find("span", class_="job-search-card__location")
        city = normalize_city(location_tag.get_text(strip=True) if location_tag else "")

        link_tag = card.find("a", class_="base-card__full-link") or card.find("a", href=True)
        source_url = link_tag.get("href", self.BASE_URL) if link_tag else self.BASE_URL
        if "?" in source_url:
            source_url = source_url.split("?")[0]

        date_tag = card.find("time")
        date_posted = date_tag.get_text(strip=True) if date_tag else None

        full_text = f"{title} {company} {city}"
        skills = extract_skills_from_text(full_text)
        track = detect_tech_track(title, full_text)

        return JobOffer(
            title=title,
            company=company,
            city=city,
            description=f"Stage PFE Informatique: {title} chez {company} ({city})",
            skills=skills,
            source_url=source_url,
            source_site="linkedin",
            domain=track,
            date_posted=date_posted,
            contract_type="Stage PFE",
        )