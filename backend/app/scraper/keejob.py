"""
keejob.py — Scraper for keejob.com

Keejob is the most structured job board in Tunisia.
Heavily used by corporate companies, consulting firms, banks,
and mid-to-large engineering/IT companies.
"""

import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_domain, normalize_city

logger = logging.getLogger(__name__)


class KeejobScraper(BaseScraper):
    BASE_URL = "https://www.keejob.com"
    # Keejob internship search query
    SEARCH_URL = "https://www.keejob.com/offres-emploi/recherche/?mots_cles=stage&page={page}"

    def scrape(self, max_pages: int = 3) -> list[JobOffer]:
        all_offers = []
        for page_num in range(1, max_pages + 1):
            url = self.SEARCH_URL.format(page=page_num)
            html = self.fetch_page(url)
            if html is None:
                break

            offers = self.parse_listing_page(html)
            if not offers:
                logger.info(f"Keejob: No more offers on page {page_num}.")
                break

            logger.info(f"Keejob page {page_num}: {len(offers)} offers")
            all_offers.extend(offers)

        logger.info(f"Keejob total: {len(all_offers)} offers scraped.")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        offers = []

        # Keejob list items
        job_cards = soup.find_all("div", class_="block_white")
        if not job_cards:
            job_cards = soup.find_all("div", class_="span9")

        if not job_cards:
            logger.warning("Keejob: No cards found.")
            return []

        for card in job_cards:
            try:
                offer = self._parse_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                logger.warning(f"Keejob card parse error: {e}")
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
        company = company_tag.get_text(strip=True) if company_tag else "Entreprise Privée"

        city_tag = card.find("span", class_="location") or card.find("i", class_="icon-map-marker")
        city_raw = city_tag.parent.get_text(strip=True) if (city_tag and city_tag.parent) else ""
        city = normalize_city(city_raw)

        full_text = card.get_text(separator=" ", strip=True)
        skills = extract_skills_from_text(full_text)
        domain = detect_domain(title, full_text)

        full_lower = full_text.lower()
        contract_type = "Stage PFE" if "pfe" in full_lower else "Stage"
        if "cdi" in full_lower:
            contract_type = "CDI"
        elif "cdd" in full_lower:
            contract_type = "CDD"

        return JobOffer(
            title=title,
            company=company,
            city=city,
            description=full_text[:1000],
            skills=skills,
            source_url=source_url,
            source_site="keejob",
            domain=domain,
            date_posted=None,
            contract_type=contract_type,
        )