from flask import Flask
from config import config_by_name
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    from app.routes.user import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp)

    # Ensure all models are imported
    from app.models import User, Museum  # Add Museum here

    # Create tables for models (if they don't exist)
    with app.app_context():
        db.create_all()

    return app