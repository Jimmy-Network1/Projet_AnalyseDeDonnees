import io
from flask import render_template, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from . import bp
from models.questionnaire import Questionnaire
from .generators import generer_csv, generer_excel, generer_pdf

@bp.route('/')
@login_required
def index():
    if current_user.role != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('dashboard.index'))
        
    questionnaires = Questionnaire.query.all()
    return render_template('export/index.html', questionnaires=questionnaires)

@bp.route('/questionnaire/<int:id>/csv')
@login_required
def exporter_csv(id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.index'))
        
    file_data, filename = generer_csv(id)
    if not file_data:
        flash('Questionnaire introuvable ou aucune donnée.', 'danger')
        return redirect(url_for('export.index'))
        
    return send_file(file_data, mimetype='text/csv', as_attachment=True, download_name=filename)

@bp.route('/questionnaire/<int:id>/excel')
@login_required
def exporter_excel(id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.index'))
        
    file_data, filename = generer_excel(id)
    if not file_data:
        flash('Questionnaire introuvable ou aucune donnée.', 'danger')
        return redirect(url_for('export.index'))
        
    return send_file(file_data, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=filename)

@bp.route('/questionnaire/<int:id>/pdf')
@login_required
def exporter_pdf(id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard.index'))
        
    file_data, filename = generer_pdf(id)
    if not file_data:
        flash('Questionnaire introuvable ou aucune donnée.', 'danger')
        return redirect(url_for('export.index'))
        
    return send_file(file_data, mimetype='application/pdf', as_attachment=True, download_name=filename)

@bp.route('/graphique/<string:chart_id>/png')
@login_required
def exporter_graphique_png(chart_id):
    # Note : L'export PNG côté serveur avec Plotly nécessite des dépendances lourdes (Kaleido ou Orca).
    # Dans une application web classique, l'export de graphiques interactifs (Plotly) 
    # se fait généralement côté client (JavaScript avec Plotly.downloadImage).
    # Nous pourrions implémenter cela dans les vues HTML directement pour éviter d'alourdir le backend.
    flash("L'export PNG des graphiques doit être effectué depuis le bouton de téléchargement intégré à chaque graphique sur le Tableau de bord.", "info")
    return redirect(url_for('dashboard.index'))
