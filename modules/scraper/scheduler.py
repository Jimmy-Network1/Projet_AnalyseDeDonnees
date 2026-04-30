from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
from .scrapers import scraper_offres_emploi, scraper_classements, scraper_actualites

# On crée une instance globale mais on ne la démarre que sur demande
scheduler = BackgroundScheduler()

def init_scheduler(app):
    """
    Initialise les jobs et lance l'ordonnanceur avec le contexte de l'application.
    Les jobs sont configurés pour s'exécuter tous les jours à 06h00, 06h05 et 06h10.
    """
    if not scheduler.running:
        # Passer l'app à l'intérieur des fonctions via args
        scheduler.add_job(
            func=scraper_offres_emploi,
            trigger=CronTrigger(hour=6, minute=0),
            args=[app],
            id='job_offres_emploi',
            replace_existing=True
        )
        
        scheduler.add_job(
            func=scraper_classements,
            trigger=CronTrigger(hour=6, minute=5),
            args=[app],
            id='job_classements',
            replace_existing=True
        )
        
        scheduler.add_job(
            func=scraper_actualites,
            trigger=CronTrigger(hour=6, minute=10),
            args=[app],
            id='job_actualites',
            replace_existing=True
        )
        
        scheduler.start()
        
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())
