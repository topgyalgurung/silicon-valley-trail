
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
                {"id": "option", "text": "Pitch", "effect": {
                    "cash": 2000,
                    "morale": -5,
                    "coffee": -3,
                    "hype": 8,
                    "bugs": 1,
                    "message": "You pitched to the local supporters and they loved it! You got a $2000 investment.",
                }},
                {"id": "skip", "text": "Skip", "effect": {
                    "cash": 0,
                    "morale": 2,
                    "coffee": 0,
                    "hype": -5,
                    "bugs": 0,
                    "message": "You skipped the pitch and the local supporters didn't like it.",
                }},
            ],
        },
    ],
    "Palo Alto": [
        {
            "key": "vc_meeting",
            "title": "VC Meeting",
            "description": "A high-stakes pitch to venture capitalists.",
            "requires_input": True,
            "options": [
                {"id": "option", "text": "meetin with a VCs", "effect": {
                    "cash": 5000,
                    "morale": -10,
                    "coffee": -5,
                    "hype": 15,
                    "bugs": 2,
                    "message": "You pitched to the VCs and they loved it! You got a $5000 investment.",
                }   },
                {"id": "skip", "text": "Skip", "effect": {
                    "cash": 0,
                    "morale": 2,
                    "coffee": 0,
                    "hype": -5,
                    "bugs": 0,
                    "message": "You skipped the pitch and the VCs didn't like it.",
                }},
            ] },
    ],
    "Mountain View": [
        {
            "key": "hackathon_sprint",
            "title": "Hackathon Sprint",
            "description": "The team pushes hard to ship features quickly.",
            "requires_input": True,
            "options": [
                {"id": "option", "text": "Sprint and ship a feature", "effect": {
                    "cash": 1000,
                    "morale": -8,
                    "coffee": -6,
                    "hype": 12,
                    "bugs": 5,
                    "message": "You sprinted and shipped a feature.",
                }},
                {"id": "skip", "text": "Skip", "effect": {
                    "cash": 0,
                    "morale": 3,
                    "coffee": 1,
                    "hype": -3,
                    "bugs": -1,
                    "message": "You skipped the sprint and the feature didn't ship.",
                }},
            ],
        },
    ],
}

ACTION_EFFECTS = {
    "travel": {
        "cash": -300,
        "coffee": -8, # stretch: calculate coffee based on distance
        "progress": 3,
    },
    "rest": {
        "morale": 10,
    },
    
    "work": {
        "cash": -100,
        "coffee": -10,
        "bugs": -5, # stretch: calculate bugs based on current bugs and work done
        "morale": -3,
    },
    "marketing": {
        "hype": 8,
        "coffee": -4,
        "morale": 3,
    },
}

