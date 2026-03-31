from game.extensions import db

# keeping common SQLAlchemy syntax for now. newer syntax uses declarative base and mapped columns.

class GameSession(db.Model):
    __tablename__ = 'game_session'

    id = db.Column(db.Integer, primary_key=True)
    current_day = db.Column(db.Integer, nullable=False, default=1)
    current_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    destination_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='in_progress') # in progress, won, lost

    progress = db.Column(db.Integer, default=0) 
    distance_traveled_miles = db.Column(db.Float, nullable=False, default=0.0)
    current_event_key = db.Column(db.String(100), nullable=True) # presented/selected event 

    # cache weather data for the current location
    # weather_summary = db.Column(db.String(100), nullable=True)
    # weather_temp_c = db.Column(db.Float, nullable=True)
    # weather_fetched_at = db.Column(db.DateTime, nullable=True)

    current_location = db.relationship(
        "Location",
        foreign_keys=[current_location_id],
        back_populates="game_sessions",
    )

    destination_location = db.relationship(
        "Location",
        foreign_keys=[destination_location_id],
        back_populates="destination_game_sessions",
    )

    # Resource columns
    cash = db.Column(db.Integer, default=50000)
    morale = db.Column(db.Integer, default=100)
    coffee = db.Column(db.Integer, default=50)
    hype = db.Column(db.Integer, default=50)
    bugs = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<GameSession {self.id}>'

class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer, unique=True)
    # latitude = db.Column(db.Float)
    # longitude = db.Column(db.Float)

    distance_to_next_miles = db.Column(db.Float, nullable=True)

    game_sessions = db.relationship(
        "GameSession",
        foreign_keys=[GameSession.current_location_id],
        back_populates="current_location",
    )

    destination_game_sessions = db.relationship(
        "GameSession",
        foreign_keys=[GameSession.destination_location_id],
        back_populates="destination_location",
    )

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Location {self.city_name}>'

