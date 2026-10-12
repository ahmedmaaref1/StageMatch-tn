"""
tunisie_travail.py — Scraper for tunisietravail.net

Tunisie Travail is one of the most widely used portals in Tunisia.
It lists PFE internships and jobs across all fields:
law firms, accounting offices, clinics, schools, manufacturing, etc.
"""

import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_domain, normalize_city

logger = logging.getLogger(__name__)


class TunisieTravailScraper(BaseScraper):
    BASE_URL = "https://www.tunisietravail.net"
    # Search URL targeting stages in Tunisia
    SEARCH_URL = "https://www.tunisietravail.net/page/{page}/?s=stage"

    def scrape(self, max_pages: int = 3) -> list[JobOffer]:
        all_offers = []
        for page_num in range(1, max_pages + 1):
            url = self.SEARCH_URL.format(page=page_num)
            html = self.fetch_page(url)
            if html is None:
                break

            offers = self.parse_listing_page(html)
            if not offers:
                logger.info(f"Tunisie Travail: No more offers on page {page_num}.")
                break

            logger.info(f"Tunisie Travail page {page_num}: {len(offers)} offers")
            all_offers.extend(offers)

        logger.info(f"Tunisie Travail total: {len(all_offers)} offers scraped.")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        offers = []

        # Tunisie Travail uses WordPress standard article post cards
        articles = soup.find_all("article")
        if not articles:
            articles = soup.find_all("div", class_="post")

        if not articles:
            logger.warning("Tunisie Travail: No article cards found.")
            return []

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
        # Title and URL
        title_tag = card.find("h2") or card.find("h3")
        if not title_tag:
            return None

        link_tag = title_tag.find("a", href=True) or card.find("a", href=True)
        title = title_tag.get_text(strip=True)
        source_url = link_tag.get("href", self.BASE_URL) if link_tag else self.BASE_URL

        # Full card text summary
        full_text = card.get_text(separator=" ", strip=True)

        # Date posted
        date_tag = card.find("time") or card.find("span", class_="entry-date")
        date_posted = date_tag.get_text(strip=True) if date_tag else None

        # Detect skills and domain using our Tunisia registry
        skills = extract_skills_from_text(full_text)
        domain = detect_domain(title, full_text)
        city = normalize_city(full_text)

        # Contract type detection
        full_lower = full_text.lower()
        contract_type = "Stage PFE" if "pfe" in full_lower else "Stage"
        if "cdi" in full_lower:
            contract_type = "CDI"
        elif "cdd" in full_lower:
            contract_type = "CDD"

        return JobOffer(
            title=title,
            company="Entreprise Tunisienne",  # Often embedded in text or anonymized
            city=city,
            description=full_text[:1000],
            skills=skills,
            source_url=source_url,
            source_site="tunisietravail",
            domain=domain,
            date_posted=date_posted,
            contract_type=contract_type,
        )