"""
keejob.py — Targeted Tech Scraper for keejob.com
Searches specifically for 'stage informatique'.
"""

import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_tech_track, normalize_city

logger = logging.getLogger(__name__)


class KeejobScraper(BaseScraper):
    BASE_URL = "https://www.keejob.com"
    SEARCH_URL = "https://www.keejob.com/offres-emploi/recherche/?mots_cles=stage+informatique&page={page}"

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

            logger.info(f"Keejob Tech page {page_num}: {len(offers)} offers")
            all_offers.extend(offers)

        logger.info(f"Keejob total tech offers: {len(all_offers)}")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        offers = []

        job_cards = soup.find_all("div", class_="block_white")
        if not job_cards:
            job_cards = soup.find_all("div", class_="span9")

        for card in job_cards:
            try:
                offer = self._parse_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                continue

        return offers

    def _parse_card(self, card) -> JobOffer | None:
        title_tag = card.find("h3") or card.find("h4")
        if not title_tag:
            return None

        title = title_tag.get_text(strip=True)
        link_tag = title_tag.find("a", href=True) or card.find("a", href=True)
        href = link_tag.get("href", "") if link_tag else ""
        source_url = href if href.startswith("http") else self.BASE_URL + href

        company_tag = card.find("a", class_="company") or card.find("span", class_="company")
        company = company_tag.get_text(strip=True) if company_tag else "Entreprise Tech Tunisie"

        city_tag = card.find("span", class_="location") or card.find("i", class_="icon-map-marker")
        city_raw = city_tag.parent.get_text(strip=True) if (city_tag and city_tag.parent) else ""
        city = normalize_city(city_raw)

        full_text = card.get_text(separator=" ", strip=True)
        skills = extract_skills_from_text(full_text)
        track = detect_tech_track(title, full_text)

        return JobOffer(
            title=title,
            company=company,
            city=city,
            description=full_text[:1000],
            skills=skills,
            source_url=source_url,
            source_site="keejob",
            domain=track,
            date_posted=None,
            contract_type="Stage PFE",
        )