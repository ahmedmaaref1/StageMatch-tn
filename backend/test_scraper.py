import logging
import sys
import os

# Add parent directory to sys.path so it can find the app module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.scraper.runner import run_all_scrapers, save_to_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)


def main():
    print("\n🕷️  StageMatch TN — Scraper Test")
    print("=" * 55)
    print("Testing 1 page across all 6 Tunisian portals...")
    print("=" * 55 + "\n")

    # Scrape 1 page per site for quick verification
    offers = run_all_scrapers(max_pages=1)

    if not offers:
        print("\n⚠️  No offers returned.")
        return

    print(f"\n🎯 Total offers collected: {len(offers)}")
    print("\n📋 Sample of offers across Tunisian domains:")
    print("-" * 55)

    # Show first 5 offers with their detected domain & skills
    for i, offer in enumerate(offers[:5], 1):
        print(f"\n[{i}] {offer['title']}")
        print(f"    🏢 Company  : {offer['company']}")
        print(f"    📍 City     : {offer['city']}")
        print(f"    🎓 Domain   : {offer['domain']}")
        print(f"    🛠️  Skills   : {', '.join(offer['skills'][:6]) or 'None detected'}")
        print(f"    🌐 Source   : {offer['source_site']}")
        print(f"    🔗 URL      : {offer['source_url'][:60]}...")

    # Save to JSON
    saved_path = save_to_json(offers)
    print(f"\n💾 Full dataset saved to: {saved_path}")
    print("\n✅ Step 1 verification complete!")


if __name__ == "__main__":
    main()