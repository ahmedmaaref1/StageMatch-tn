"""
app/scheduler.py — Automated 24h Background Scraping & Alert Service
"""

import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.database import SessionLocal
from app.models.offer import Offer
from app.scraper.runner import run_all_scrapers

logger = logging.getLogger("stagematch.scheduler")

# État de surveillance en mémoire (monitoring dashboard)
scheduler_state = {
    "is_active": False,
    "last_run": None,
    "last_status": "En attente du premier cycle",
    "last_inserted_count": 0,
    "last_scraped_count": 0,
    "next_run": None,
    "last_error": None,
}

scheduler = BackgroundScheduler()


def run_scheduled_scraping():
    """
    Tâche de fond : scrape les portails d'emploi tunisiens et enregistre
    uniquement les nouvelles offres technologiques dans PostgreSQL.
    """
    logger.info("⏰ [CRON] Démarrage de la tâche de scraping automatique planifiée...")
    scheduler_state["last_status"] = "En cours d'exécution..."
    scheduler_state["last_run"] = datetime.now().isoformat()
    scheduler_state["last_error"] = None

    db = SessionLocal()
    inserted = 0
    scraped_total = 0

    try:
        # Scrape les portails Tanitjobs, Tunisie Travail et LinkedIn
        raw_offers = run_all_scrapers(max_pages=2)
        scraped_total = len(raw_offers)

        # Anti-doublons robuste : charge tous les URLs existants en mémoire
        seen_urls = set(u[0] for u in db.query(Offer.source_url).all() if u[0])

        for item in raw_offers:
            source_url = item.get("source_url")
            if not source_url or source_url in seen_urls:
                continue

            # Marquer l'URL comme vue pour éviter les doublons intra-batch
            seen_urls.add(source_url)

            new_offer = Offer(
                title=item.get("title", "Stage PFE"),
                company=item.get("company", "Entreprise Tech"),
                city=item.get("city", "Tunisie"),
                domain=item.get("domain", "Général"),
                contract_type=item.get("contract_type", "Stage PFE"),
                description=item.get("description", ""),
                skills=item.get("skills", []),
                source_url=source_url,
                source_site=item.get("source_site", "scraper"),
                date_posted=item.get("date_posted", "Récemment"),
            )
            db.add(new_offer)
            inserted += 1

        db.commit()
        total_in_db = db.query(Offer).count()

        scheduler_state["last_status"] = "Succès"
        scheduler_state["last_inserted_count"] = inserted
        scheduler_state["last_scraped_count"] = scraped_total
        logger.info(
            f"✅ [CRON] Scraping terminé avec succès ! "
            f"{inserted} nouvelles offres ajoutées (Total en base: {total_in_db})."
        )

    except Exception as e:
        db.rollback()
        scheduler_state["last_status"] = "Erreur"
        scheduler_state["last_error"] = str(e)
        logger.error(f"❌ [CRON] Échec du scraping planifié : {e}")

    finally:
        # Toujours fermer la session de base de données pour éviter les fuites de mémoire
        db.close()
        job = scheduler.get_job("daily_tech_scraping")
        if job and job.next_run_time:
            scheduler_state["next_run"] = job.next_run_time.isoformat()


def start_scheduler():
    """
    Initialise et lance le planificateur de tâches en arrière-plan.
    Exécution programmée toutes les 24h à 02:00 du matin (heure de Tunis).
    """
    if not scheduler.running:
        # CronTrigger : tourne tous les jours à 02h00
        trigger = CronTrigger(hour=2, minute=0)
        
        scheduler.add_job(
            run_scheduled_scraping,
            trigger=trigger,
            id="daily_tech_scraping",
            name="Scraping quotidien PFE Tunisie (24h)",
            replace_existing=True,
        )
        scheduler.start()
        scheduler_state["is_active"] = True

        job = scheduler.get_job("daily_tech_scraping")
        if job and job.next_run_time:
            scheduler_state["next_run"] = job.next_run_time.isoformat()

        logger.info(f"🚀 [SCHEDULER] Planificateur démarré. Prochaine exécution : {scheduler_state['next_run']}")


def shutdown_scheduler():
    """
    Arrête proprement le thread du planificateur lorsque FastAPI s'arrête.
    """
    if scheduler.running:
        scheduler.shutdown(wait=False)
        scheduler_state["is_active"] = False
        logger.info("🛑 [SCHEDULER] Planificateur arrêté proprement.")


def get_scheduler_status():
    """
    Renvoie les métriques actuelles pour l'API et le tableau de bord frontend.
    """
    job = scheduler.get_job("daily_tech_scraping")
    if job and job.next_run_time:
        scheduler_state["next_run"] = job.next_run_time.isoformat()
    return scheduler_state
