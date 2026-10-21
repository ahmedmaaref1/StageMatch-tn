"""
tanitjobs.py — Targeted Tech Scraper for tanitjobs.com
Searches specifically for 'stage informatique' / Tech PFE offers.
"""

import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_tech_track, normalize_city

logger = logging.getLogger(__name__)


class TanitJobsScraper(BaseScraper):
    BASE_URL = "https://www.tanitjobs.com"
    # Targeted search for IT / Software internships
    SEARCH_URL = "https://www.tanitjobs.com/jobs/?keyword=stage+informatique&page={page}"

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
            logger.info(f"TanitJobs Tech page {page_num}: {len(offers)} offers")
            all_offers.extend(offers)

        logger.info(f"TanitJobs total tech offers: {len(all_offers)}")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        offers = []

        job_cards = soup.find_all("div", class_="sj-job-card")
        if not job_cards:
            job_cards = soup.find_all("div", class_="listing-item__jobs")

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
        title_tag = card.find("div", class_="sj-card-title")
        if not title_tag:
            return None

        link_tag = title_tag.find("a", href=True)
        title = link_tag.get_text(strip=True) if link_tag else title_tag.get_text(strip=True)
        href = link_tag.get("href", "") if link_tag else ""
        source_url = href if href.startswith("http") else self.BASE_URL + href

        company_tag = card.find("div", class_="sj-card-company")
        if company_tag:
            company_link = company_tag.find("a")
            company = company_link.get_text(strip=True) if company_link else company_tag.get_text(strip=True)
            if "·" in company:
                company = company.split("·")[0].strip()
        else:
            company = "Entreprise Tech Tunisie"

        loc_tag = card.find("span", class_="sj-loc")
        city = normalize_city(loc_tag.get_text(strip=True) if loc_tag else "")

        desc_tag = card.find("div", class_="sj-card-desc")
        description = desc_tag.get_text(strip=True) if desc_tag else title

        type_tag = card.find("span", class_="sj-type")
        contract_type = type_tag.get_text(strip=True) if type_tag else "Stage PFE"

        date_tag = card.find("span", class_="sj-card-date")
        date_posted = date_tag.get_text(strip=True) if date_tag else None

        full_text = f"{title} {description} {company}"
        skills = extract_skills_from_text(full_text)
        track = detect_tech_track(title, full_text)

        return JobOffer(
            title=title,
            company=company,
            city=city,
            description=description[:1000],
            skills=skills,
            source_url=source_url,
            source_site="tanitjobs",
            domain=track,  # Now assigns one of our 6 Tech Tracks!
            date_posted=date_posted,
            contract_type=contract_type,
        )