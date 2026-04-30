from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class DiplomeForm(FlaskForm):
    intitule = StringField('Intitulé du diplôme', validators=[DataRequired(), Length(max=255)], description="Ex: Licence en Informatique, Master en Droit...")
    etablissement = StringField('Établissement ou Université', validators=[DataRequired(), Length(max=255)], description="Ex: Université de Yaoundé I, Polytechnique...")
    annee_obtention = IntegerField('Année d\'obtention', validators=[DataRequired(), NumberRange(min=1980, max=2030)], description="Ex: 2024")
    statut_insertion = SelectField('Statut professionnel actuel', validators=[DataRequired()], choices=[
        ('', '-- Sélectionnez votre situation --'),
        ('En emploi (CDI)', 'En emploi (CDI)'),
        ('En emploi (CDD)', 'En emploi (CDD)'),
        ('En stage', 'En stage professionnel'),
        ('En recherche d\'emploi', 'En recherche d\'emploi (Chômage)'),
        ('En poursuite d\'études', 'En poursuite d\'études'),
        ('Entrepreneur / Indépendant', 'Entrepreneur / Indépendant'),
        ('Autre', 'Autre')
    ])
    submit = SubmitField('Ajouter le diplôme')