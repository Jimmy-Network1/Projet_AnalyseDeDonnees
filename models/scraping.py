from models import db
from datetime import datetime

class ScrapingJob(db.Model):
    __tablename__ = 'scraping_jobs'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='en_attente')
    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)
    
    # Relations
    data = db.relationship('ScrapingData', backref='job', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ScrapingJob {self.id} - {self.source} ({self.status})>"

class ScrapingData(db.Model):
    __tablename__ = 'scraping_data'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('scraping_jobs.id'), nullable=False)
    titre = db.Column(db.String(255), nullable=True)
    contenu = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ScrapingData {self.id} from Job {self.job_id}>"
