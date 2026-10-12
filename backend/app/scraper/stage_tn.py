"""
stage_tn.py — Scraper for stage.tn (100% dedicated to internships in Tunisia)
"""

import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_domain, normalize_city

logger = logging.getLogger(__name__)


class StageTnScraper(BaseScraper):
    BASE_URL = "https://www.stage.tn"
    SEARCH_URL = "https://www.stage.tn/offres-de-stages/?fwp_paged={page}"

    def scrape(self, max_pages: int = 3) -> list[JobOffer]:
        all_offers = []
        for page_num in range(1, max_pages + 1):
            url = self.SEARCH_URL.format(page=page_num)
            html = self.fetch_page(url)
            if html is None:
                break

            offers = self.parse_listing_page(html)
            if not offers:
                break

            logger.info(f"Stage.tn page {page_num}: {len(offers)} offers")
            all_offers.extend(offers)

        logger.info(f"Stage.tn total: {len(all_offers)} offers scraped.")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        offers = []

        cards = soup.find_all("div", class_="facetwp-template")
        if cards:
            job_items = cards[0].find_all("article") or cards[0].find_all("div", class_="job-item")
        else:
            job_items = soup.find_all("article")

        for card in job_items:
            try:
                offer = self._parse_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                logger.warning(f"Stage.tn parse error: {e}")
                continue

        return offers

    def _parse_card(self, card) -> JobOffer | None:
        title_tag = card.find("h2") or card.find("h3")
        if not title_tag:
            return None

        title = title_tag.get_text(strip=True)
        link_tag = title_tag.find("a", href=True) or card.find("a", href=True)
        source_url = link_tag.get("href", self.BASE_URL) if link_tag else self.BASE_URL

        company_tag = card.find("span", class_="company") or card.find("div", class_="company")
        company = company_tag.get_text(strip=True) if company_tag else "Entreprise en Tunisie"

        full_text = card.get_text(separator=" ", strip=True)
        city = normalize_city(full_text)
        skills = extract_skills_from_text(full_text)
        domain = detect_domain(title, full_text)

        return JobOffer(
            title=title,
            company=company,
            city=city,
            description=full_text[:1000],
            skills=skills,
            source_url=source_url,
            source_site="stage_tn",
            domain=domain,
            date_posted=None,
            contract_type="Stage PFE",
        )