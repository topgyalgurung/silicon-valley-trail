import logging

from flask import Flask
from flask_cors import CORS

from .extensions import db, migrate
from .config import Config, config as config_map
from . import routes

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

    app.register_blueprint(routes.game_routes)
    register_error_handlers(app)

    if not app.config.get('TESTING'):
        with app.app_context(): 
            db.create_all()
            from data.seed_data import seed_locations
            seed_locations()
            logger.info("Database seeded successfully")

    return app

def register_error_handlers(app):
    """register custom error handlers for the application"""
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource Not Found'}, 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return {'error': 'Internal Server Error'}, 500