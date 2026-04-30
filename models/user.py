from models import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='utilisateur')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    reponses = db.relationship('Reponse', backref='user', lazy=True)
    diplomes = db.relationship('Diplome', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.nom} ({self.email})>"
