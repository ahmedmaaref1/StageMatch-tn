import time
import logging
import requests
from abc import ABC, abstractmethod
from typing import Optional
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobOffer:
    def __init__(
        self,
        title: str,
        company: str,
        city: str,
        description: str,
        skills: list[str],
        source_url: str,
        source_site: str,
        domain: str = "General",
        date_posted: Optional[str] = None,
        contract_type: Optional[str] = None,
    ):
        self.title = title
        self.company = company
        self.city = city
        self.description = description
        self.skills = skills
        self.source_url = source_url
        self.source_site = source_site
        self.domain = domain
        self.date_posted = date_posted
        self.contract_type = contract_type

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "company": self.company,
            "city": self.city,
            "description": self.description,
            "skills": self.skills,
            "source_url": self.source_url,
            "source_site": self.source_site,
            "domain": self.domain,
            "date_posted": self.date_posted,
            "contract_type": self.contract_type,
        }

    def __repr__(self):
        return f"<JobOffer: {self.title} @ {self.company} [{self.domain}]>"


class BaseScraper(ABC):
    def __init__(self, delay_seconds: float = 2.0):
        self.delay_seconds = delay_seconds
        self.ua = UserAgent()
        self.session = requests.Session()

    def _get_headers(self) -> dict:
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-TN,fr;q=0.9,en;q=0.8,ar;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    def fetch_page(self, url: str) -> Optional[str]:
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            time.sleep(self.delay_seconds)
            return response.text
        except requests.exceptions.Timeout:
            logger.error(f"Timeout: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP {e.response.status_code}: {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    @abstractmethod
    def scrape(self, max_pages: int = 3) -> list[JobOffer]:
        pass

    @abstractmethod
    def parse_listing_page(self, html: str) -> list[JobOffer]:
        pass