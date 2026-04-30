from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class InscriptionForm(FlaskForm):
    nom = StringField('Nom complet', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirmation_mdp = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('mot_de_passe', message='Les mots de passe doivent correspondre.')])
    submit = SubmitField("S'inscrire")

class ConnexionForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField("Se connecter")
