from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class QuestionnaireForm(FlaskForm):
    titre = StringField('Titre du questionnaire', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description')
    submit = SubmitField('Créer le questionnaire')
