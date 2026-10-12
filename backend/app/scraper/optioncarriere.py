import logging
from bs4 import BeautifulSoup
from .base import BaseScraper, JobOffer
from .skills_registry import extract_skills_from_text, detect_domain, normalize_city

logger = logging.getLogger(__name__)


class OptionCarriereScraper(BaseScraper):
    BASE_URL = "https://www.optioncarriere.tn"
    SEARCH_URL = "https://www.optioncarriere.tn/recherche/emplois?s=stage&l=Tunisie&p={page}"
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
            logger.info(f"Optioncarriere page {page_num}: {len(offers)} offers")
            all_offers.extend(offers)
        logger.info(f"Optioncarriere total: {len(all_offers)}")
        return all_offers

    def parse_listing_page(self, html: str) -> list[JobOffer]:
        soup = BeautifulSoup(html, "lxml")
        job_cards = soup.find_all("article", class_="job_preview")
        if not job_cards:
            job_cards = soup.find_all("div", class_="job")
        if not job_cards:
            logger.warning("Optioncarriere: no cards found")
            return []
        offers = []
        for card in job_cards:
            try:
                offer = self._parse_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                logger.warning(f"Card parse error: {e}")
        return offers

    def _parse_card(self, card) -> JobOffer | None:
        title_tag = card.find("h2") or card.find("h3")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown"

        company_tag = card.find("span", class_="company") or card.find("p", class_="company")
        company = company_tag.get_text(strip=True) if company_tag else "Unknown"

        location_tag = card.find("span", class_="location") or card.find("li", class_="location")
        city = normalize_city(location_tag.get_text(strip=True) if location_tag else "")

        link_tag = card.find("a", href=True)
        href = link_tag.get("href", "") if link_tag else ""
        source_url = href if href.startswith("http") else self.BASE_URL + href

        date_tag = card.find("time") or card.find("span", class_="date")
        date_posted = date_tag.get_text(strip=True) if date_tag else None

        full_text = card.get_text(separator=" ", strip=True)
        skills = extract_skills_from_text(full_text)
        domain = detect_domain(title, full_text)

        return JobOffer(
            title=title, company=company, city=city,
            description=full_text[:1000], skills=skills,
            source_url=source_url, source_site="optioncarriere",
            domain=domain, date_posted=date_posted,
            contract_type="Stage PFE",
        )