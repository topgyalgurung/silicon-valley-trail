from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .config import Config
from . import routes

def create_app():
    """
    Application factory function.

    Creates and configures the Flask application instance using
    a modular architecture with blueprints. Extensions are initialized
    without storing application-specific state globally.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    CORS(app)

    try:
        app.config.from_object(Config) # configure app with config 
    except IOError:
        print("Error loading config: .env file not found")
        raise

    db.init_app(app) 
    migrate.init_app(app, db)

    # register blueprints for route modularization
    app.register_blueprint(routes.game_routes)

    # register error handlers and request callbacks 

    @app.route("/test/")
    def test_page():
        return '<h1> Testing the Flask Application Factory Pattern</h1>'

    # configure logging 

    # create database tables within app context(dev only)
    with app.app_context(): 
        db.create_all()
        from data.seed_data import seed_locations
        seed_locations()
        print("Database seeded successfully")

    return app

