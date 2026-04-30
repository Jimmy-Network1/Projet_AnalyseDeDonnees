from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import bp
from .forms import InscriptionForm, ConnexionForm
from models import db
from models.user import User

@bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index')) # Assuming dashboard has an index route
        
    form = InscriptionForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(email=form.email.data).first()
        if user_exists:
            flash('Un compte avec cet email existe déjà.', 'danger')
            return redirect(url_for('auth.inscription'))
            
        hashed_password = generate_password_hash(form.mot_de_passe.data)
        nouveau_user = User(nom=form.nom.data, email=form.email.data, mot_de_passe_hash=hashed_password)
        db.session.add(nouveau_user)
        db.session.commit()
        
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.connexion'))
        
    return render_template('auth/inscription.html', form=form)

@bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index')) # Assuming dashboard has an index route
        
    form = ConnexionForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.mot_de_passe_hash, form.mot_de_passe.data):
            login_user(user)
            flash('Connexion réussie !', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/') # Redirect to home or dashboard
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
            
    return render_template('auth/connexion.html', form=form)

@bp.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.connexion'))
