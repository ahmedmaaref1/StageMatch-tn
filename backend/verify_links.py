"""
verify_links.py — Checks HTTP status of all offer application links in the database.
"""
import requests
import sys
import os
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.database import SessionLocal
from app.models.offer import Offer

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_url(offer):
    url = offer.source_url
    try:
        resp = requests.head(url, headers=HEADERS, timeout=6, allow_redirects=True)
        if resp.status_code in [403, 404, 405]:
            resp = requests.get(url, headers=HEADERS, timeout=6, stream=True, allow_redirects=True)
        return offer.id, offer.company, offer.title, url, resp.status_code
    except Exception:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=6, stream=True, allow_redirects=True)
            return offer.id, offer.company, offer.title, url, resp.status_code
        except Exception as e2:
            return offer.id, offer.company, offer.title, url, f"Error ({type(e2).__name__})"

def main():
    db = SessionLocal()
    offers = db.query(Offer).all()
    print(f"\n🔍 Checking {len(offers)} offers in database...")

    working = 0
    broken = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_url, offers)

        for offer_id, company, title, url, status in results:
            if isinstance(status, int) and 200 <= status < 400:
                working += 1
                print(f"  🟢 [{status}] {company[:20]:<20} -> {url[:60]}")
            else:
                broken += 1
                print(f"  🔴 [{status}] {company[:20]:<20} -> {url}")

    print("\n" + "=" * 60)
    print(f"📊 SUMMARY: {working} working links, {broken} broken/404 links")
    print("=" * 60)
    db.close()

if __name__ == "__main__":
    main()