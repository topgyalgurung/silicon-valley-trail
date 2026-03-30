from game.extensions import db
from game.models import Location

LOCATIONS = [
    {
        "city_name": "San Jose",
        "description": "Your startup humble garage, HQ",
        "order_index": 1,
        "distance_to_next_miles": 6,
    },
    {
        "city_name": "Santa Clara",
        "description": "Early-stage hustle with small wins and supply stops.",
        "order_index": 2,
        "distance_to_next_miles": 5,
    },
    {
        "city_name": "Sunnyvale",
        "description": "Angels, heat, and quick decisions define this stop.",
        "order_index": 3,
        "distance_to_next_miles": 6,
    },
    {
        "city_name": "Mountain View",
        "description": "Engineering grind and hackathon energy.",
        "order_index": 4,
        "distance_to_next_miles": 7,
    },
    {
        "city_name": "Palo Alto",
        "description": "High-stakes VC meetings and networking.",
        "order_index": 5,
        "distance_to_next_miles": 3,
    },
    {
        "city_name": "Menlo Park",
        "description": "Strategic decisions and team dynamics matter here.",
        "order_index": 6,
        "distance_to_next_miles": 5,
    },
    {
        "city_name": "Redwood City",
        "description": "Operational challenges and supply opportunities.",
        "order_index": 7,
        "distance_to_next_miles": 6,
    },
    {
        "city_name": "San Mateo",
        "description": "Fatigue sets in, but momentum builds.",
        "order_index": 8,
        "distance_to_next_miles": 4,
    },
    {
        "city_name": "Burlingame",
        "description": "Unexpected encounters and quick recovery stops.",
        "order_index": 9,
        "distance_to_next_miles": 3,
    },
    {
        "city_name": "San Bruno",
        "description": "Final preparation before the last push.",
        "order_index": 10,
        "distance_to_next_miles": 4,
    },
    {
        "city_name": "Daly City",
        "description": "Pressure rises as the destination nears.",
        "order_index": 11,
        "distance_to_next_miles": 5,
    },
    {
        "city_name": "San Francisco",
        "description": "Destination reached. Time to pitch your startup.",
        "order_index": 12,
        "distance_to_next_miles": 0,
    },
]
def seed_locations():
    for data in LOCATIONS:
        exists = {loc.city_name for loc in Location.query.all()}
        new_locations = [Location(**loc) for loc in LOCATIONS if loc["city_name"] not in exists]
        if new_locations:
            db.session.add_all(new_locations)
            db.session.commit()

if __name__ == "__main__":
    from game import create_app

    print("Seeding locations...")
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_locations()  
        print("Locations seeded successfully")

