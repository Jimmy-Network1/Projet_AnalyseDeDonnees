from flask import Blueprint

bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire')

from . import routes
