import logging

from flask import Flask
from flask_cors import CORS

from .extensions import db, migrate
from .config import Config, config as config_map
from game.routes import game_routes
from game.errors import errors_bp

logger = logging.getLogger(__name__)

def create_app(config_name="default"):
    """
    Application factory function.

    Creates and configures the Flask application instance using
    a modular architecture with blueprints. Extensions are initialized
    without storing application-specific state globally. help avoid circular imports.
    """
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(config_map.get(config_name, Config)) # configure app with config 

    db.init_app(app) 
    migrate.init_app(app, db)

    app.register_blueprint(game_routes)
    app.register_blueprint(errors_bp)

    if not app.config.get('TESTING'):
        with app.app_context(): 
            db.create_all()
            from data.seed_data import seed_locations
            seed_locations()
            logger.info("Database seeded successfully")

    return app
