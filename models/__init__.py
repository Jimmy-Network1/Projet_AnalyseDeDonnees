from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .questionnaire import Questionnaire, Question, Reponse, ReponseDetail
from .scraping import ScrapingJob, ScrapingData
from .diplome import Diplome
