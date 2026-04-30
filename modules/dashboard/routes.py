from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import bp
from models.questionnaire import Questionnaire, Reponse
from models.scraping import ScrapingData
from models.diplome import Diplome
from .charts import graphique_taux_reponse, graphique_insertion_pro, graphique_evolution, graphique_offres_emploi

@bp.route('/')
@login_required
def index():
    if current_user.role != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('dashboard.public'))
        
    chart_reponse = graphique_taux_reponse()
    chart_insertion = graphique_insertion_pro()
    chart_evolution = graphique_evolution()
    chart_offres = graphique_offres_emploi()
    
    return render_template('dashboard/index.html', 
                           chart_reponse=chart_reponse,
                           chart_insertion=chart_insertion,
                           chart_evolution=chart_evolution,
                           chart_offres=chart_offres)

@bp.route('/public')
def public():
    chart_reponse = graphique_taux_reponse()
    chart_insertion = graphique_insertion_pro()
    
    stats = {
        'total_questionnaires': Questionnaire.query.count(),
        'total_reponses': Reponse.query.count(),
        'total_offres': ScrapingData.query.count()
    }
    
    return render_template('dashboard/public.html', 
                           chart_reponse=chart_reponse, 
                           chart_insertion=chart_insertion,
                           stats=stats)
