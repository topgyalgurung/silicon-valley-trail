from flask import Flask
from game.extensions import db
from game.config import Config
from game import pages


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(pages.game_routes)

    with app.app_context():
        db.create_all()

    return app

