from flask import Flask
from flask_cors import CORS
from game.extensions import db
from game.config import Config
from game import pages


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config) # configure app with config 

    db.init_app(app) # initialize app with extension 

    app.register_blueprint(pages.game_routes)

    with app.app_context(): 
        db.create_all()

    return app

