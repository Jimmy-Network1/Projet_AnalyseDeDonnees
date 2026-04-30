from flask import Blueprint

bp = Blueprint('scraper', __name__, url_prefix='/scraper')

from . import routes
