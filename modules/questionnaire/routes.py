from flask import render_template, redirect, url_for, flash, request, make_response
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from . import bp
from .forms import QuestionnaireForm
from models import db
from models.questionnaire import Questionnaire, Question, Reponse, ReponseDetail

# Helper to generate dynamic form for answering
def get_answer_form(questionnaire):
    class DynamicForm(FlaskForm):
        pass
        
    for q in questionnaire.questions:
        field_name = f'q_{q.id}'
        if q.type == 'texte':
            setattr(DynamicForm, field_name, TextAreaField(q.texte, validators=[DataRequired()]))
        elif q.type == 'qcm':
            choices = [(opt.strip(), opt.strip()) for opt in (q.options or '').split(',') if opt.strip()]
            setattr(DynamicForm, field_name, SelectField(q.texte, choices=choices, validators=[DataRequired()]))
        elif q.type == 'echelle_1_10':
            setattr(DynamicForm, field_name, IntegerField(q.texte, validators=[DataRequired(), NumberRange(min=1, max=10)]))
        elif q.type == 'date':
            setattr(DynamicForm, field_name, DateField(q.texte, validators=[DataRequired()]))

    setattr(DynamicForm, 'submit', SubmitField('Soumettre mes réponses'))
    return DynamicForm()

@bp.route('/creer', methods=['GET', 'POST'])
@login_required
def creer():
    if current_user.role != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = QuestionnaireForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Parsing manual form fields for questions
        titre = form.titre.data
        description = form.description.data
        
        nouveau_questionnaire = Questionnaire(titre=titre, description=description)
        db.session.add(nouveau_questionnaire)
        db.session.flush() # To get the ID
        
        # Parse questions
        q_textes = request.form.getlist('q_texte[]')
        q_types = request.form.getlist('q_type[]')
        q_options = request.form.getlist('q_options[]')
        
        for i in range(len(q_textes)):
            if q_textes[i].strip():
                question = Question(
                    questionnaire_id=nouveau_questionnaire.id,
                    texte=q_textes[i],
                    type=q_types[i],
                    options=q_options[i] if q_types[i] == 'qcm' else None
                )
                db.session.add(question)
                
        db.session.commit()
        flash('Questionnaire créé avec succès.', 'success')
        return redirect(url_for('questionnaire.liste'))

    return render_template('questionnaire/creer.html', form=form)

@bp.route('/liste')
@login_required
def liste():
    if current_user.role != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('dashboard.index'))
        
    questionnaires = Questionnaire.query.order_by(Questionnaire.created_at.desc()).all()
    return render_template('questionnaire/liste.html', questionnaires=questionnaires)

@bp.route('/<int:id>/repondre', methods=['GET'])
def repondre(id):
    questionnaire = Questionnaire.query.get_or_404(id)
    
    # Vérification double soumission par cookie
    if request.cookies.get(f'answered_q_{id}'):
        flash('Vous avez déjà répondu à ce questionnaire.', 'info')
        return render_template('questionnaire/deja_repondu.html', questionnaire=questionnaire)
        
    # Vérification double soumission par DB (si connecté)
    if current_user.is_authenticated:
        reponse_existante = Reponse.query.filter_by(questionnaire_id=id, user_id=current_user.id).first()
        if reponse_existante:
            flash('Vous avez déjà répondu à ce questionnaire.', 'info')
            return render_template('questionnaire/deja_repondu.html', questionnaire=questionnaire)

    form = get_answer_form(questionnaire)
    return render_template('questionnaire/repondre.html', questionnaire=questionnaire, form=form)

@bp.route('/<int:id>/soumettre', methods=['POST'])
def soumettre(id):
    questionnaire = Questionnaire.query.get_or_404(id)
    
    # Vérifications anti double-soumission (Cookie et DB)
    if request.cookies.get(f'answered_q_{id}'):
        flash('Vous avez déjà répondu à ce questionnaire.', 'danger')
        return redirect(url_for('questionnaire.repondre', id=id))

    if current_user.is_authenticated:
        if Reponse.query.filter_by(questionnaire_id=id, user_id=current_user.id).first():
            flash('Vous avez déjà répondu à ce questionnaire.', 'danger')
            return redirect(url_for('questionnaire.repondre', id=id))

    form = get_answer_form(questionnaire)
    
    if form.validate_on_submit():
        nouvelle_reponse = Reponse(
            questionnaire_id=id,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(nouvelle_reponse)
        db.session.flush()
        
        for q in questionnaire.questions:
            field_name = f'q_{q.id}'
            if field_name in form.data:
                valeur = str(form.data[field_name])
                detail = ReponseDetail(
                    reponse_id=nouvelle_reponse.id,
                    question_id=q.id,
                    valeur=valeur
                )
                db.session.add(detail)
                
        db.session.commit()
        
        flash('Merci pour votre participation !', 'success')
        
        # Set cookie
        resp = make_response(redirect(url_for('questionnaire.repondre', id=id)))
        resp.set_cookie(f'answered_q_{id}', '1', max_age=60*60*24*365) # 1 year
        return resp
        
    return render_template('questionnaire/repondre.html', questionnaire=questionnaire, form=form)

@bp.route('/<int:id>/resultats')
@login_required
def resultats(id):
    if current_user.role != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('dashboard.index'))
        
    questionnaire = Questionnaire.query.get_or_404(id)
    reponses = Reponse.query.filter_by(questionnaire_id=id).all()
    
    return render_template('questionnaire/resultats.html', questionnaire=questionnaire, reponses=reponses)
