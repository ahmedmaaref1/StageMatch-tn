"""
tanitjobs.py — Updated Scraper for tanitjobs.com
Updated to match Tanitjobs' new 'sj-job-card' HTML design!
"""

import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_domain, normalize_city

logger = logging.getLogger(__name__)


class TanitJobsScraper(BaseScraper):
    BASE_URL = "https://www.tanitjobs.com"
    SEARCH_URL = "https://www.tanitjobs.com/jobs/?keyword=stage&page={page}"

    def scrape(self, max_pages: int = 3) -> list[JobOffer]:
        all_offers = []
        for page_num in range(1, max_pages + 1):
            url = self.SEARCH_URL.format(page=page_num)
            html = self.fetch_page(url)
            if html is None:
                break
            offers = self.parse_listing_page(html)
            if not offers:
                logger.info(f"TanitJobs: No offers found on page {page_num}.")
                break
            logger.info(f"TanitJobs page {page_num}: {len(offers)} offers")
            all_offers.extend(offers)

        logger.info(f"TanitJobs total: {len(all_offers)} offers scraped.")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        offers = []

        # New Tanitjobs card class: sj-job-card
        job_cards = soup.find_all("div", class_="sj-job-card")

        # Fallback to older classes if any
        if not job_cards:
            job_cards = soup.find_all("div", class_="listing-item__jobs")

        if not job_cards:
            logger.warning("TanitJobs: no cards found — selectors may need updating")
            return []

        for card in job_cards:
            try:
                offer = self._parse_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                logger.warning(f"TanitJobs card parse error: {e}")
                continue

        return offers

    def _parse_card(self, card) -> JobOffer | None:
        # Title & URL
        title_tag = card.find("div", class_="sj-card-title")
        if not title_tag:
            return None

        link_tag = title_tag.find("a", href=True)
        title = link_tag.get_text(strip=True) if link_tag else title_tag.get_text(strip=True)
        href = link_tag.get("href", "") if link_tag else ""
        source_url = href if href.startswith("http") else self.BASE_URL + href

        # Company
        company_tag = card.find("div", class_="sj-card-company")
        if company_tag:
            company_link = company_tag.find("a")
            company = company_link.get_text(strip=True) if company_link else company_tag.get_text(strip=True)
            # Remove any trailing city text if attached to company tag
            if "·" in company:
                company = company.split("·")[0].strip()
        else:
            company = "Entreprise sur Tanitjobs"

        # City / Location
        loc_tag = card.find("span", class_="sj-loc")
        city_raw = loc_tag.get_text(strip=True) if loc_tag else ""
        city = normalize_city(city_raw)

        # Description
        desc_tag = card.find("div", class_="sj-card-desc")
        description = desc_tag.get_text(strip=True) if desc_tag else title

        # Contract Type (CDI, CDD, Stage...)
        type_tag = card.find("span", class_="sj-type")
        contract_type = type_tag.get_text(strip=True) if type_tag else "Stage"

        # Date
        date_tag = card.find("span", class_="sj-card-date")
        date_posted = date_tag.get_text(strip=True) if date_tag else None

        # Full text for skills & domain detection
        full_text = f"{title} {description} {city_raw}"
        skills = extract_skills_from_text(full_text)
        domain = detect_domain(title, full_text)

        return JobOffer(
            title=title,
            company=company,
            city=city,
            description=description[:1000],
            skills=skills,
            source_url=source_url,
            source_site="tanitjobs",
            domain=domain,
            date_posted=date_posted,
            contract_type=contract_type,
        )