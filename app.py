import os
import click
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from config import config_dict
from models import db
from models.user import User

# Extensions initialization
login_manager = LoginManager()
login_manager.login_view = 'auth.connexion'
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
login_manager.login_message_category = "info"

csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Initialize scheduler
    from modules.scraper.scheduler import init_scheduler
    # Pour éviter le double lancement par l'autoreloader de Werkzeug (en dev)
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        init_scheduler(app)

    # Register blueprints
    from modules.auth import bp as auth_bp
    from modules.questionnaire import bp as questionnaire_bp
    from modules.scraper import bp as scraper_bp
    from modules.dashboard import bp as dashboard_bp
    from modules.export import bp as export_bp
    from modules.user import bp as user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(questionnaire_bp)
    app.register_blueprint(scraper_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(user_bp)

    # Initialize DB automatically on startup
    with app.app_context():
        db.create_all()
        # Check if admin exists
        admin = User.query.filter_by(email='admin@academiscan.local').first()
        if not admin:
            hashed_pw = generate_password_hash('admin123')
            admin = User(nom='Administrateur', email='admin@academiscan.local', mot_de_passe_hash=hashed_pw, role='admin')
            db.session.add(admin)
            db.session.commit()
            print('Base de données initialisée automatiquement.')

    # Simple route for '/' to redirect to public dashboard
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('dashboard.public'))

    # CLI Command to init DB
    @app.cli.command("init-db")
    def init_db_command():
        """Créer les tables et un utilisateur admin."""
        db.create_all()
        
        # Check if admin exists
        admin = User.query.filter_by(email='admin@academiscan.local').first()
        if not admin:
            hashed_pw = generate_password_hash('admin123')
            admin = User(nom='Administrateur', email='admin@academiscan.local', mot_de_passe_hash=hashed_pw, role='admin')
            db.session.add(admin)
            db.session.commit()
            click.echo('Base de données initialisée et compte admin créé (admin@academiscan.local / admin123).')
        else:
            click.echo('La base de données est déjà initialisée.')

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=app.config.get('DEBUG', True))
