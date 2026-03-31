INITIAL_GAME_STATE = {
    "current_day": 1,
    "status": "in_progress",
    "cash": 50000, 
    "morale": 100, # 0-100
    "coffee": 50, # if stays 0 for 2 turn -> lose
    "hype": 50,  # 0-100
    "bugs": 0,
    "progress": 0, # 0-100
    "current_event_key": None,
}

EVENTS_BY_LOCATION = {
    "Santa Clara": [
        {
            "id": "sc_coffee_cart",
            "name": "Coffee Cart",
            "description": "A local coffee cart offers startup discounts.",
            "requires_input": True,
            "options": [
                {"id": "buy", "text": "Buy coffee", "effect": {"money": -50, "coffee": 20}},
                {"id": "skip", "text": "Skip it", "effect": {"morale": -2}}
            ]
        },
        {
            "id": "sc_rain_commute",
            "name": "Rainy Commute",
            "description": "Rain slows the team and drains energy.",
            "requires_input": False,
            "weather_conditions": ["Rain"],
            "effect": {"coffee": -10, "morale": -5}
        },
        {
            "id": "sc_quick_bugfix",
            "name": "Quick Bug Fix Sprint",
            "description": "A few focused hours could reduce bugs.",
            "requires_input": True,
            "condition": {"bugs": {"min": 4}},
            "options": [
                {"id": "fix", "text": "Fix bugs", "effect": {"bugs": -4, "coffee": -8}},
                {"id": "ignore", "text": "Ignore for now", "effect": {"bugs": 2}}
            ]
        }
    ],

    "Sunnyvale": [
        {
            "id": "sv_angel_pitch",
            "name": "Angel Investor Sighting",
            "description": "A small angel investor gives you a chance to pitch.",
            "requires_input": True,
            "options": [
                {"id": "pitch", "text": "Pitch now", "effect": {"money": 250, "hype": 5, "morale": 3}},
                {"id": "skip", "text": "Skip it", "effect": {"morale": -3}}
            ]
        },
        {
            "id": "sv_heatwave",
            "name": "Heatwave Grind",
            "description": "The heat makes everyone irritable and tired.",
            "requires_input": False,
            "weather_conditions": ["Clear", "Sunny"],
            "effect": {"coffee": -8, "morale": -6}
        },
        {
            "id": "sv_supply_run",
            "name": "Supply Run",
            "description": "You can detour for snacks and coffee.",
            "requires_input": True,
            "options": [
                {"id": "restock", "text": "Restock", "effect": {"money": -80, "coffee": 15, "morale": 4}},
                {"id": "move_on", "text": "Move on", "effect": {"morale": -2}}
            ]
        }
    ],

    "Mountain View": [
        {
            "id": "mv_hackathon",
            "name": "Hackathon Invite",
            "description": "A local hackathon could move the product forward fast.",
            "requires_input": True,
            "options": [
                {"id": "join", "text": "Join the hackathon", "effect": {"coffee": -15, "bugs": 4, "hype": 6}},
                {"id": "skip", "text": "Skip it", "effect": {"morale": -2}}
            ]
        },
        {
            "id": "mv_cloudy_focus",
            "name": "Cloudy Focus Day",
            "description": "A quiet gray day helps the team focus.",
            "requires_input": False,
            "weather_conditions": ["Clouds"],
            "effect": {"morale": 2}
        },
        {
            "id": "mv_demo_crash",
            "name": "Demo Crash",
            "description": "A live demo crashes and hurts confidence.",
            "requires_input": True,
            "options": [
                {"id": "patch", "text": "Patch immediately", "effect": {"bugs": -3, "coffee": -10, "morale": 2}},
                {"id": "pivot", "text": "Spin the narrative", "effect": {"hype": 4, "morale": -4}}
            ]
        }
    ],

    "Palo Alto": [
        {
            "id": "pa_vc_pitch",
            "name": "VC Pitch Opportunity",
            "description": "A top VC gives you five minutes to pitch.",
            "requires_input": True,
            "options": [
                {"id": "pitch", "text": "Pitch confidently", "effect": {"money": 600, "hype": 10, "morale": -5}},
                {"id": "decline", "text": "Decline", "effect": {"morale": 2}}
            ]
        },
        {
            "id": "pa_clear_founder_meetup",
            "name": "Founder Meetup in the Sun",
            "description": "Good weather brings founders and investors outside.",
            "requires_input": True,
            "weather_conditions": ["Clear", "Sunny"],
            "options": [
                {"id": "join", "text": "Join the meetup", "effect": {"hype": 8, "morale": 5, "coffee": -5}},
                {"id": "skip", "text": "Stay focused", "effect": {}}
            ]
        },
        {
            "id": "pa_rain_delay",
            "name": "Rainy Traffic Delay",
            "description": "Rainy roads delay the team and kill momentum.",
            "requires_input": False,
            "weather_conditions": ["Rain"],
            "effect": {"coffee": -10, "morale": -8}
        }
    ],

    "Menlo Park": [
        {
            "id": "mp_partner_intro",
            "name": "Warm Partner Intro",
            "description": "A founder friend offers a VC partner introduction.",
            "requires_input": True,
            "options": [
                {"id": "take_intro", "text": "Take the intro", "effect": {"hype": 10, "money": 300, "morale": 4}},
                {"id": "decline_intro", "text": "Decline politely", "effect": {"morale": -2}}
            ]
        },
        {
            "id": "mp_team_argument",
            "name": "Team Argument",
            "description": "A disagreement breaks out over product direction.",
            "requires_input": True,
            "options": [
                {"id": "mediate", "text": "Pause and mediate", "effect": {"morale": 8}},
                {"id": "push", "text": "Push through it", "effect": {"morale": -10}}
            ]
        },
        {
            "id": "mp_fog_misread",
            "name": "Foggy Investor Misread",
            "description": "Bad weather and worse timing make the room feel cold.",
            "requires_input": False,
            "weather_conditions": ["Fog", "Mist"],
            "effect": {"morale": -6, "hype": -4}
        }
    ],

    "Redwood City": [
        {
            "id": "rc_server_outage",
            "name": "Server Outage",
            "description": "A production issue spikes bugs.",
            "requires_input": True,
            "condition": {"bugs": {"min": 6}},
            "options": [
                {"id": "fix", "text": "Fix bugs", "effect": {"bugs": -6, "coffee": -12, "morale": -3}},
                {"id": "delay_fix", "text": "Delay the fix", "effect": {"bugs": 8}}
            ]
        },
        {
            "id": "rc_supply_deal",
            "name": "Supplier Discount",
            "description": "A local supplier offers a limited-time deal.",
            "requires_input": True,
            "options": [
                {"id": "buy", "text": "Buy supplies", "effect": {"money": -120, "coffee": 18, "morale": 3}},
                {"id": "skip", "text": "Skip the deal", "effect": {"morale": -1}}
            ]
        },
        {
            "id": "rc_windy_detour",
            "name": "Windy Detour",
            "description": "Strong winds and chaos cost the team time and coffee.",
            "requires_input": False,
            "weather_conditions": ["Wind", "Windy"],
            "effect": {"coffee": -8}
        }
    ],

    "San Mateo": [
        {
            "id": "sm_burnout",
            "name": "Team Burnout",
            "description": "The team is exhausted and morale dips.",
            "requires_input": True,
            "options": [
                {"id": "rest", "text": "Force a rest day", "effect": {"morale": 10, "coffee": 5}},
                {"id": "push", "text": "Push through", "effect": {"morale": -12}}
            ]
        },
        {
            "id": "sm_demo_day",
            "name": "Demo Day Invite",
            "description": "A small demo day could boost hype.",
            "requires_input": True,
            "options": [
                {"id": "present", "text": "Present the product", "effect": {"hype": 12, "money": 200, "coffee": -5}},
                {"id": "pass", "text": "Pass for now", "effect": {"morale": -2}}
            ]
        },
        {
            "id": "sm_cloud_cover",
            "name": "Cloud Cover Productivity",
            "description": "A gloomy day keeps distractions low and focus high.",
            "requires_input": False,
            "weather_conditions": ["Clouds"],
            "effect": {"bugs": -2}
        }
    ],

    "Burlingame": [
        {
            "id": "bu_airport_lead",
            "name": "Airport Investor Lead",
            "description": "You bump into a promising investor on the move.",
            "requires_input": True,
            "options": [
                {"id": "chase", "text": "Chase the lead", "effect": {"money": 350, "hype": 6, "coffee": -6}},
                {"id": "ignore", "text": "Ignore and focus", "effect": {}}
            ]
        },
        {
            "id": "bu_supplies",
            "name": "Emergency Refill",
            "description": "A quick stop can replenish coffee.",
            "requires_input": True,
            "options": [
                {"id": "refill", "text": "Refill supplies", "effect": {"money": -90, "coffee": 20}},
                {"id": "skip", "text": "Skip refill", "effect": {"morale": -3}}
            ]
        },
        {
            "id": "bu_fog_fatigue",
            "name": "Foggy Fatigue",
            "description": "Low visibility and stress sap the team’s energy.",
            "requires_input": False,
            "weather_conditions": ["Fog", "Mist"],
            "effect": {"coffee": -9, "morale": -7}
        }
    ],

    "San Bruno": [
        {
            "id": "sb_launch_prep",
            "name": "Launch Prep Sprint",
            "description": "The team can sprint toward launch, but it will hurt.",
            "requires_input": True,
            "options": [
                {"id": "sprint", "text": "Sprint hard", "effect": {"coffee": -12, "bugs": 5}},
                {"id": "steady", "text": "Keep a steady pace", "effect": {"morale": 2}}
            ]
        },
        {
            "id": "sb_press_ping",
            "name": "Local Press Ping",
            "description": "A small media mention could boost hype.",
            "requires_input": True,
            "options": [
                {"id": "respond", "text": "Respond quickly", "effect": {"hype": 10, "coffee": -4}},
                {"id": "ignore", "text": "Ignore it", "effect": {}}
            ]
        },
        {
            "id": "sb_clear_run",
            "name": "Clear-Sky Momentum",
            "description": "Great weather helps the team move cleanly into the final stretch.",
            "requires_input": False,
            "weather_conditions": ["Clear", "Sunny"],
            "effect": {"morale": 3}
        }
    ],

    "Daly City": [
        {
            "id": "dc_final_nerves",
            "name": "Final Stretch Nerves",
            "description": "Pressure rises as the destination gets close.",
            "requires_input": True,
            "options": [
                {"id": "pep_talk", "text": "Give a pep talk", "effect": {"morale": 8}},
                {"id": "push_forward", "text": "Push forward fast", "effect": {"morale": -6}}
            ]
        },
        {
            "id": "dc_supply_cache",
            "name": "Hidden Supply Cache",
            "description": "You find a stash of useful startup fuel.",
            "requires_input": True,
            "options": [
                {"id": "take", "text": "Take supplies", "effect": {"coffee": 15, "morale": 4}},
                {"id": "leave", "text": "Leave it", "effect": {"hype": 2}}
            ]
        },
        {
            "id": "dc_fog_delay",
            "name": "Fog Delay",
            "description": "The famous fog makes the final approach feel much longer.",
            "requires_input": False,
            "weather_conditions": ["Fog", "Mist"],
            "effect": {"coffee": -6, "morale": -5}
        }
    ],

    "San Francisco": [
        {
        
        }
    ]
}

ACTION_EFFECTS = {
    "travel": {
        "cash": -300,
        "coffee": -8, # stretch: calculate coffee based on distance
    },
    "rest": {
        "morale": 10,
        "coffee": -5,
        "message": "You rested and recovered your morale and coffee.",
    },
    
    "work": {
        "coffee": -10,
        "bugs": -5, # stretch: calculate bugs based on current bugs and work done
        "morale": -6, 
        "message": "You worked on the product and reduced bugs.",
    },
    "marketing": {
        "hype": 8,
        "cash": -100,
        "message": "You pushed a marketing campaign and increased hype.",
    },
}

MOCK_WEATHER = {
    "san jose": "Clear",
    "santa clara": "Sunny",
    "sunnyvale": "Clouds",
    "mountain view": "Rain",
    "palo alto": "Clear",
    "menlo park": "Clouds",
    "redwood city": "Windy",
    "san mateo": "Clouds",
    "burlingame": "Clear",
    "san bruno": "Fog",
    "daly city": "Fog",
    "san francisco": "Fog",
}

WEATHER_EFFECTS = {
    "Rain": {"cash": -200, "morale": -3, "coffee": -5},
    "Fog": {"morale": -2, "coffee": -3},
    "Clouds": {"morale": -1},
    "Windy": {"coffee": -2, "morale": -2},
    "Clear": {},
    "Sunny": {"morale": 2},
}

RESOURCE_LIMITS = {
    "cash": {"min": 0, "max": None},
    "morale": {"min": 0, "max": 100},
    "coffee": {"min": 0, "max": None},
    "hype": {"min": 0, "max": 100},
    "bugs": {"min": 0, "max": None},  
}

COFFEE_WARNING_EVENT = {
    "id": "system_coffee_warning",
    "name": "Coffee Crisis",
    "description": "Your coffee supply is about to run out! Refuel now or risk losing 2 days.",
    "requires_input": True,
    "options": [
        {
            "id": "replenish",
            "text": "Replenish coffee (otherwise miss 2 turns)",
            "effect": {"coffee": 25, "skip_turns": 1}, # no skip turns if replenish coffee
        },
        {
            "id": "risk_it",
            "text": "Risk it and continue",
            "effect": {"coffee": 0, "skip_turns": 2},
        },
    ],
}