from game.extensions import db

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, default=1)
    current_location_index = db.Column(db.Integer, default=0)
    city = db.Column(db.String(100), nullable=False, default="San Jose")
    current_location_detail = db.Column(
        db.String(255),
        nullable=False,
        default="San Jose is the capital of California"
    )
    is_active = db.Column(db.Boolean, default=True)
    coffee_zero_turns = db.Column(db.Integer, default=0)

    money = db.Column(db.Integer, default=50000)
    morale = db.Column(db.Integer, default=100)
    coffee = db.Column(db.Integer, default=50)
    hype = db.Column(db.Integer, default=50)
    bugs = db.Column(db.Integer, default=0)
    progress = db.Column(db.Integer, default=0)

    current_event_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"<GameSession id={self.id} city={self.city} day={self.day}>"

