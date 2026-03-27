EVENTS_BY_LOCATION = {
    "San Jose": [
        {
            "key": "coffee_run",
            "title": "Coffee Supply Run",
            "description": "You spend some cash to restock coffee for the team.",
            "effects": {
                "cash": -300,
                "morale": 5,
                "coffee": 10,
                "hype": 0,
                "bugs": 0,
            },
        },
        {
            "key": "quick_pitch",
            "title": "Quick Local Pitch",
            "description": "You pitch local supporters and gain some cash, but the team gets tired.",
            "effects": {
                "cash": 2000,
                "morale": -5,
                "coffee": -3,
                "hype": 8,
                "bugs": 1,
            },
        },
    ],
    "Palo Alto": [
        {
            "key": "vc_meeting",
            "title": "VC Meeting",
            "description": "A promising VC meeting gives your startup momentum.",
            "effects": {
                "cash": 5000,
                "morale": -10,
                "coffee": -5,
                "hype": 15,
                "bugs": 2,
            },
        }
    ],
    "Mountain View": [
        {
            "key": "hackathon_sprint",
            "title": "Hackathon Sprint",
            "description": "The team ships features fast, but technical debt grows.",
            "effects": {
                "cash": 1000,
                "morale": -8,
                "coffee": -6,
                "hype": 12,
                "bugs": 5,
            },
        }
    ],
}