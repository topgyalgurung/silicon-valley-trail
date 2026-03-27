# data/mock_api_data.py

INITIAL_GAME_STATE = {
    "day": 1,
    "current_location_index": 0,
    "is_active": True,
    "current_event": None,
    "coffee_zero_turns": 0,
    "team": {
        "cash": 50000,
        "morale": 100,   # 0-100
        "coffee": 50,    # if stays 0 for 2 turns -> lose
        "hype": 50,      # 0-100
        "bugs": 0,
        "progress": 0    # 0-100 percentage
    }
}

LOCATIONS = [
    "San Jose",
    "Santa Clara",
    "Sunnyvale",
    "Mountain View",
    "Palo Alto",
    "Menlo Park",
    "Redwood City",
    "San Mateo",
    "Burlingame",
    "San Bruno",
    "Daly City",
    "San Francisco"
]

EVENTS = [
    {
        "id": "investor_pitch",
        "name": "Investor Pitch",
        "description": "You meet an investor. Pitch your idea?",
        "requires_input": True,
        "options": [
            {
                "id": "pitch",
                "text": "Pitch confidently",
                "effect": {
                    "cash": 5000,
                    "hype": 10,
                    "morale": 5
                }
            },
            {
                "id": "decline",
                "text": "Decline politely",
                "effect": {
                    "morale": -5,
                    "hype": -5
                }
            }
        ]
    },
    {
        "id": "hackathon",
        "name": "Hackathon Weekend",
        "description": "A local hackathon could boost your product, but the team will burn caffeine fast.",
        "requires_input": True,
        "options": [
            {
                "id": "join",
                "text": "Join the hackathon",
                "effect": {
                    "progress": 15,
                    "coffee": -15,
                    "bugs": 5,
                    "hype": 10
                }
            },
            {
                "id": "skip",
                "text": "Skip and stay focused",
                "effect": {
                    "morale": -3
                }
            }
        ]
    },
    {
        "id": "server_fire",
        "name": "Production Fire",
        "description": "A critical bug hits production and the team scrambles to respond.",
        "requires_input": False,
        "effect": {
            "bugs": 12,
            "progress": -5,
            "coffee": -10,
            "morale": -8
        }
    },
    {
        "id": "coffee_sponsor",
        "name": "Coffee Sponsor",
        "description": "A local coffee shop offers free cold brew for startup founders.",
        "requires_input": True,
        "options": [
            {
                "id": "accept",
                "text": "Take the free coffee",
                "effect": {
                    "coffee": 20,
                    "morale": 5
                }
            },
            {
                "id": "decline",
                "text": "Decline and keep moving",
                "effect": {
                    "hype": 2
                }
            }
        ]
    },
    {
        "id": "team_argument",
        "name": "Team Argument",
        "description": "A disagreement breaks out about product direction.",
        "requires_input": True,
        "options": [
            {
                "id": "mediate",
                "text": "Pause and mediate",
                "effect": {
                    "morale": 8,
                    "progress": -3
                }
            },
            {
                "id": "push_forward",
                "text": "Ignore it and keep shipping",
                "effect": {
                    "progress": 5,
                    "morale": -10
                }
            }
        ]
    },
    {
        "id": "demo_day",
        "name": "Demo Day Invite",
        "description": "You are invited to present at a small founder demo day.",
        "requires_input": True,
        "options": [
            {
                "id": "present",
                "text": "Present the product",
                "effect": {
                    "hype": 12,
                    "cash": 2000,
                    "coffee": -5
                }
            },
            {
                "id": "pass",
                "text": "Pass for now",
                "effect": {
                    "morale": -2
                }
            }
        ]
    },
    {
        "id": "quiet_day",
        "name": "Quiet Day",
        "description": "Nothing dramatic happens today. The team keeps moving.",
        "requires_input": False,
        "effect": {
            "progress": 2
        }
    }
]

MOCK_WEATHER = {
    "San Jose": "Clear",
    "Santa Clara": "Sunny",
    "Sunnyvale": "Clouds",
    "Mountain View": "Rain",
    "Palo Alto": "Clear",
    "Menlo Park": "Clouds",
    "Redwood City": "Windy",
    "San Mateo": "Clouds",
    "Burlingame": "Clear",
    "San Bruno": "Fog",
    "Daly City": "Fog",
    "San Francisco": "Fog"
}

ACTION_EFFECTS = {
    "travel": {
        "cash": -300,
        "coffee": -8,
        "progress": 3
    },
    "work": {
        "cash": 1000,
        "coffee": -10,
        "progress": 8,
        "bugs": 3,
        "morale": -3
    },
    "rest": {
        "morale": 10,
        "coffee": 8
    },
    "network": {
        "hype": 8,
        "coffee": -4,
        "morale": 3
    }
}