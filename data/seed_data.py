from game.extensions import db
from game.models import Location
from game import create_app

LOCATIONS = [
    {
        "city_name": "San Jose",
        "description": "Your startup's humble garage HQ.",
        "order_index": 1,
    },
    {
        "city_name": "Santa Clara",
        "description": "A tech-heavy stop with potential opportunities.",
        "order_index": 2,
        
    },
    {
        "city_name": "Palo Alto",
        "description": "Investor meetings and startup energy everywhere.",
        "order_index": 3,
    },
    {
        "city_name": "Menlo Park",
        "description": "A place to network and regroup.",
        "order_index": 4,
    },
    {
        "city_name": "Mountain View",
        "description": "Hackathon and engineering grind zone.",
        "order_index": 5,
    },
    {
        "city_name": "Redwood City",
        "description": "A midpoint stop to recover supplies.",
        "order_index": 6,
    },
    {
        "city_name": "San Mateo",
        "description": "Momentum builds as the team gets closer.",
        "order_index": 7,
    },
    {
        "city_name": "Burlingame",
        "description": "A quick rest before the final push north.",
        "order_index": 8,
    },
    {
        "city_name": "South San Francisco",
        "description": "Final stretch with pressure rising.",
        "order_index": 9,
    },
    {
        "city_name": "San Francisco",
        "description": "Destination reached. Time to pitch.",
        "order_index": 10,
    },
]

def seed_locations():
    for data in LOCATIONS:
        exists = Location.query.filter_by(city_name=data["city_name"]).first()
        if not exists: # insert only if location does not exist
            location = Location(**data)
            db.session.add(location)
            db.session.commit()

if __name__ == "__main__":
    print("Seeding locations...")
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_locations()  
        print("Locations seeded successfully")
        db.session.close()
        exit(0)
