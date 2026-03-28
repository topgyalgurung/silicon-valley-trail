EVENTS_BY_LOCATION = {
    "San Jose": [
        {
            "key": "coffee_run",
            "title": "Coffee Supply Run",
            "description": "You spend some cash to restock coffee for the team.",
            "requires_input": False,
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
            "description": "You pitch local supporters.",
            "requires_input": True,
            "options": [
                {"id": "pitch", "text": "Pitch"},
                {"id": "skip", "text": "Skip"},
            ],
            "outcomes": {
                "pitch": {
                    "cash": 2000,
                    "morale": -5,
                    "coffee": -3,
                    "hype": 8,
                    "bugs": 1,
                },
                "skip": {
                    "cash": 0,
                    "morale": 0,
                    "coffee": 0,
                    "hype": -2,
                    "bugs": 0,
                },
            },
        },
    ],

    "Palo Alto": [
        {
            "key": "vc_meeting",
            "title": "VC Meeting",
            "description": "A high-stakes pitch to venture capitalists.",
            "requires_input": True,
            "options": [
                {"id": "pitch", "text": "Pitch"},
                {"id": "skip", "text": "Skip"},
            ],
            "outcomes": {
                "pitch": {
                    "cash": 5000,
                    "morale": -10,
                    "coffee": -5,
                    "hype": 15,
                    "bugs": 2,
                    "message": "You pitched to the VCs and they loved it! You got a $5000 investment.",
                },
                "skip": {
                    "cash": 0,
                    "morale": 2,
                    "coffee": 0,
                    "hype": -5,
                    "bugs": 0,
                },
            },
        },
        
    ],

    "Mountain View": [
        {
            "key": "hackathon_sprint",
            "title": "Hackathon Sprint",
            "description": "The team pushes hard to ship features quickly.",
            "requires_input": True,
            "options": [
                {"id": "sprint", "text": "Sprint"},
                {"id": "skip", "text": "Skip"},
            ],
            "outcomes": {
                "sprint": {
                    "cash": 1000,
                    "morale": -8,
                    "coffee": -6,
                    "hype": 12,
                    "bugs": 5,
                },
                "skip": {
                    "cash": 0,
                    "morale": 3,
                    "coffee": 1,
                    "hype": -3,
                    "bugs": -1,
                },
            },
        },
    ],
}

