# auto discover by pytest

import pytest
from game import create_app
from game.config import TestingConfig
from game.extensions import db
from game.models import Location, GameSession

@pytest.fixture() # run before each test function
def app():

    
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        # seed location data
        locations = [
            Location(city_name="San Jose", order_index=1, description="Start city"),
            Location(city_name="Santa Clara", order_index=2, description="Next stop"),
            Location(city_name="Sunnyvale", order_index=3, description="Third stop"),
            Location(city_name="San Francisco", order_index=12, description="Destination"),
        ]
        db.session.add_all(locations)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

    # clean up / reset resources here
    

@pytest.fixture()
def client(app):
    """create test client """
    return app.test_client()

@pytest.fixture()
def runner(app):
    """ create test CLI runner """
    return app.test_cli_runner()


@pytest.fixture
def sample_game(app):
    """Return a fresh game session for unit tests."""
    start_location = Location.query.filter_by(city_name="San Jose").first()
    destination_location = Location.query.filter_by(city_name="San Francisco").first()

    game = GameSession(
        current_day=1,
        current_location_id=start_location.id,
        destination_location_id=destination_location.id,
        cash=500,
        morale=80,
        coffee=50,
        hype=40,
        bugs=10,
        progress=0,
        status="in_progress",
        current_event_key=None,
    )

    db.session.add(game)
    db.session.commit()
    return game