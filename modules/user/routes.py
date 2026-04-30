from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import bp
from models import db
from models.diplome import Diplome
from models.questionnaire import Reponse
from .forms import DiplomeForm

@bp.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    form = DiplomeForm()
    
    if form.validate_on_submit():
        nouveau_diplome = Diplome(
            user_id=current_user.id,
            intitule=form.intitule.data,
            etablissement=form.etablissement.data,
            annee_obtention=form.annee_obtention.data,
            statut_insertion=form.statut_insertion.data
        )
        db.session.add(nouveau_diplome)
        db.session.commit()
        flash('Votre diplôme et votre statut ont été ajoutés avec succès !', 'success')
        return redirect(url_for('user.profil'))
        
    # Récupérer les diplômes de l'utilisateur
    diplomes = Diplome.query.filter_by(user_id=current_user.id).order_by(Diplome.annee_obtention.desc()).all()
    
    # Récupérer l'historique de ses réponses aux questionnaires
    historique_reponses = Reponse.query.filter_by(user_id=current_user.id).order_by(Reponse.submitted_at.desc()).all()
    
    return render_template('user/profil.html', 
                           form=form, 
                           diplomes=diplomes, 
                           historique_reponses=historique_reponses)

@bp.route('/diplome/<int:id>/supprimer', methods=['POST'])
@login_required
def supprimer_diplome(id):
    diplome = Diplome.query.get_or_404(id)
    
    # Vérification de sécurité : l'utilisateur ne peut supprimer que SES diplômes
    if diplome.user_id != current_user.id and current_user.role != 'admin':
        flash('Action non autorisée.', 'danger')
        return redirect(url_for('user.profil'))
        
    db.session.delete(diplome)
    db.session.commit()
    flash('Le diplôme a été supprimé.', 'success')
    return redirect(url_for('user.profil'))
