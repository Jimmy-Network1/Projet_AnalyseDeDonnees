from models import db
from datetime import datetime

class Diplome(db.Model):
    __tablename__ = 'diplomes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    intitule = db.Column(db.String(255), nullable=False)
    etablissement = db.Column(db.String(255), nullable=False)
    annee_obtention = db.Column(db.Integer, nullable=False)
    statut_insertion = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Diplome {self.intitule} ({self.annee_obtention})>"
