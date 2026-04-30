from models import db
from datetime import datetime

class Questionnaire(db.Model):
    __tablename__ = 'questionnaires'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    questions = db.relationship('Question', backref='questionnaire', lazy=True, cascade="all, delete-orphan")
    reponses = db.relationship('Reponse', backref='questionnaire', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Questionnaire {self.titre}>"

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaires.id'), nullable=False)
    texte = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50), nullable=False) # ex: 'texte', 'choix_multiple'
    options = db.Column(db.String(500), nullable=True) # Options séparées par des virgules pour QCM
    
    # Relations
    reponse_details = db.relationship('ReponseDetail', backref='question', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Question {self.texte[:20]}>"

class Reponse(db.Model):
    __tablename__ = 'reponses'
    id = db.Column(db.Integer, primary_key=True)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaires.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    details = db.relationship('ReponseDetail', backref='reponse', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Reponse {self.id} for Questionnaire {self.questionnaire_id}>"

class ReponseDetail(db.Model):
    __tablename__ = 'reponse_details'
    id = db.Column(db.Integer, primary_key=True)
    reponse_id = db.Column(db.Integer, db.ForeignKey('reponses.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    valeur = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ReponseDetail {self.id} (Reponse: {self.reponse_id}, Question: {self.question_id})>"
