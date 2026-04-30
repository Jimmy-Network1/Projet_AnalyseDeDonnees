import threading
from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from . import bp
from models import db
from models.scraping import ScrapingJob, ScrapingData
from .scrapers import scraper_offres_emploi, scraper_classements, scraper_actualites

@bp.route('/lancer', methods=['POST'])
@login_required
def lancer():
    if current_user.role != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('dashboard.index'))
        
    app = current_app._get_current_object()
    
    # Exécution asynchrone via des threads pour ne pas bloquer la requête
    threading.Thread(target=scraper_offres_emploi, args=(app,), daemon=True).start()
    threading.Thread(target=scraper_classements, args=(app,), daemon=True).start()
    threading.Thread(target=scraper_actualites, args=(app,), daemon=True).start()
    
    flash("Scraping manuel lancé en arrière-plan. Vous pouvez consulter les logs d'ici quelques instants.", 'info')
    return redirect(url_for('scraper.logs'))

@bp.route('/logs')
@login_required
def logs():
    if current_user.role != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('dashboard.index'))
        
    jobs = ScrapingJob.query.order_by(ScrapingJob.started_at.desc()).all()
    return render_template('scraper/logs.html', jobs=jobs)
