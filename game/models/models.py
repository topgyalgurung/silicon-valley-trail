from game.extensions import db

# keeping common SQLAlchemy syntax for now. newer syntax uses declarative base and mapped columns.

class GameSession(db.Model):
    __tablename__ = 'game_session'

    id = db.Column(db.Integer, primary_key=True)
    current_day = db.Column(db.Integer, nullable=False, default=1)
    current_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    destination_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='in_progress') # in progress, won, lost

    progress = db.Column(db.Integer, nullable=False, default=0) # percentage of the way to the destination
    distance_traveled_miles = db.Column(db.Float, nullable=False, default=0.0)
    coffee_zero_turns = db.Column(db.Integer, default=0)
    current_event_key = db.Column(db.String(100), nullable=True) # presented/selected event 

    # Resource columns
    cash = db.Column(db.Integer, default=50000)
    morale = db.Column(db.Integer, default=100)
    coffee = db.Column(db.Integer, default=50)
    hype = db.Column(db.Integer, default=50)
    bugs = db.Column(db.Integer, default=0)

    current_location = db.relationship('Location', foreign_keys=[current_location_id])
    destination_location = db.relationship('Location', foreign_keys=[destination_location_id])
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<GameSession %r>' % self.id

class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer, unique=True)
    # latitude = db.Column(db.Float)
    # longitude = db.Column(db.Float)

    # distance from this city to next city 
    distance_to_next_miles = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return '<Location %r>' % self.city_name

