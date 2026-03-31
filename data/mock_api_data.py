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
            "name": "Discount Coffee Cart",
            "description": "A local coffee cart offers a startup founder special.",
            "requires_input": True,
            "options": [
                {
                    "id": "buy",
                    "text": "Buy extra coffee",
                    "effect": {"cash": -80, "coffee": 20, "morale": 2, "bugs": 2}
                },
                {
                    "id": "skip",
                    "text": "Save cash and move on",
                    "effect": {"morale": -2}
                }
            ]
        },
        {
            "id": "sc_quick_bugfix",
            "name": "Quick Bug Fix Sprint",
            "description": "A focused work session could clean up part of the product, but it will drain the team.",
            "requires_input": True,
            "condition": {"bugs": {"min": 4}},
            "options": [
                {
                    "id": "fix",
                    "text": "Fix the bugs now",
                    "effect": {"bugs": -4, "coffee": -8, "morale": -2}
                },
                {
                    "id": "delay",
                    "text": "Delay the fix",
                    "effect": {"bugs": 2, "morale": 1}
                }
            ]
        },
        {
            "id": "sc_student_demo",
            "name": "Campus Demo Invite",
            "description": "A student group invites you to demo your product. It could boost momentum, but it takes time and energy.",
            "requires_input": True,
            "options": [
                {
                    "id": "demo",
                    "text": "Do the demo",
                    "effect": {"hype": 6, "morale": 3, "coffee": -5, "bugs": 1}
                },
                {
                    "id": "pass",
                    "text": "Stay focused on the roadmap",
                    "effect": {"bugs": -1, "coffee": -2, "morale": -1}
                }
            ]
        }
    ],

    "Sunnyvale": [
        {
            "id": "sv_angel_pitch",
            "name": "Angel Investor Sighting",
            "description": "A small angel investor offers you one shot to pitch.",
            "requires_input": True,
            "options": [
                {
                    "id": "pitch",
                    "text": "Pitch immediately",
                    "effect": {"cash": 250, "hype": 5, "morale": 2, "bugs": 2}
                },
                {
                    "id": "skip",
                    "text": "Skip and conserve energy",
                    "effect": {"coffee": 3, "morale": -2}
                }
            ]
        },
        {
            "id": "sv_supply_run",
            "name": "Supply Run",
            "description": "You can detour for snacks and coffee before the next push.",
            "requires_input": True,
            "options": [
                {
                    "id": "restock",
                    "text": "Restock supplies",
                    "effect": {"cash": -100, "coffee": 18, "morale": 4}
                },
                {
                    "id": "move_on",
                    "text": "Keep moving",
                    "effect": {"morale": -3}
                }
            ]
        },
        {
            "id": "sv_founder_advice",
            "name": "Founder Advice Session",
            "description": "An experienced founder offers feedback. Listening could improve your product, but it delays the schedule.",
            "requires_input": True,
            "options": [
                {
                    "id": "listen",
                    "text": "Take the advice",
                    "effect": {"bugs": 2, "morale": 2, "coffee": -4}
                },
                {
                    "id": "ignore",
                    "text": "Trust your instincts",
                    "effect": {"hype": 3, "bugs": 1}
                }
            ]
        }
    ],

    "Mountain View": [
        {
            "id": "mv_hackathon",
            "name": "Hackathon Invite",
            "description": "A local hackathon could accelerate your product, but the team may burn out.",
            "requires_input": True,
            "options": [
                {
                    "id": "join",
                    "text": "Join the hackathon",
                    "effect": {"hype": 8, "bugs": 3, "coffee": -12, "morale": -2}
                },
                {
                    "id": "skip",
                    "text": "Skip and keep building steadily",
                    "effect": {"bugs": -1, "morale": 1}
                }
            ]
        },
        {
            "id": "mv_demo_crash",
            "name": "Demo Crash",
            "description": "A live demo goes sideways. You can either fix the issue or salvage the narrative.",
            "requires_input": True,
            "options": [
                {
                    "id": "patch",
                    "text": "Patch it immediately",
                    "effect": {"bugs": -3, "coffee": -10, "morale": 2}
                },
                {
                    "id": "pivot",
                    "text": "Spin the story",
                    "effect": {"hype": 5, "morale": -4, "bugs": 1}
                }
            ]
        },
        {
            "id": "mv_recruiter_ping",
            "name": "Recruiter Ping",
            "description": "A talented engineer might join your team if you can impress them.",
            "requires_input": True,
            "options": [
                {
                    "id": "recruit",
                    "text": "Spend time recruiting",
                    "effect": {"morale": 4, "cash": -120, "bugs": -2}
                },
                {
                    "id": "decline",
                    "text": "Keep your team lean",
                    "effect": {"morale": -1}
                }
            ]
        }
    ],

    "Palo Alto": [
        {
            "id": "pa_vc_pitch",
            "name": "VC Pitch Opportunity",
            "description": "A top VC offers you five minutes. Big upside, but high pressure.",
            "requires_input": True,
            "options": [
                {
                    "id": "pitch",
                    "text": "Take the pitch",
                    "effect": {"cash": 600, "hype": 10, "morale": -5}
                },
                {
                    "id": "decline",
                    "text": "Protect the team’s energy",
                    "effect": {"morale": 3}
                }
            ]
        },
        {
            "id": "pa_founder_meetup",
            "name": "Founder Meetup",
            "description": "A packed founder meetup could create buzz, but it will consume valuable energy.",
            "requires_input": True,
            "options": [
                {
                    "id": "network",
                    "text": "Work the room",
                    "effect": {"hype": 9, "morale": 4, "coffee": -6}
                },
                {
                    "id": "focus",
                    "text": "Skip and keep building",
                    "effect": {"bugs": -2}
                }
            ]
        },
        {
            "id": "pa_investor_buzz",
            "name": "Investor Buzz",
            "description": "Online chatter around your startup is trending upward.",
            "requires_input": True,
            "condition":{
                 "hype": {"min": 55},
                "cash": {"min": 150}
            },
            "api_condition": {
                "weather_main": {"in": ["Clear", "Clouds", "Sunny"]}
            },
            "options": [
                {
                    "id": "capitalize",
                    "text": "Lean into the momentum",
                    "effect": {"hype": 10, "coffee": -4, "cash":-100}
                },
                {
                    "id": "stay_measured",
                    "text": "Stay disciplined",
                    "effect": {"morale": 3}
                }
            ]
        }
    ],

    "Menlo Park": [
        {
            "id": "mp_partner_intro",
            "name": "Warm Partner Intro",
            "description": "A founder friend offers a VC partner introduction.",
            "requires_input": True,
            "options": [
                {
                    "id": "take_intro",
                    "text": "Take the intro",
                    "effect": {"hype": 10, "cash": 250, "morale": 4}
                },
                {
                    "id": "decline_intro",
                    "text": "Decline politely",
                    "effect": {"morale": -2}
                }
            ]
        },
        {
            "id": "mp_team_argument",
            "name": "Team Argument",
            "description": "A disagreement breaks out over product direction.",
            "requires_input": True,
            "options": [
                {
                    "id": "mediate",
                    "text": "Pause and mediate",
                    "effect": {"morale": 8, "coffee": -4}
                },
                {
                    "id": "push",
                    "text": "Push through the conflict",
                    "effect": {"morale": -10, "hype": 2}
                }
            ]
        },
        {
            "id": "mp_bad_commute",
            "name": "Bad Commute",
            "description": "The team arrives drained after a rough travel day.",
            "requires_input": True,
            "api_condition": {
                "weather_main": {"in": ["Rain", "Thunderstorm"]}
            },
            "options": [
                {
                    "id": "rest",
                    "text": "Take recovery time",
                    "effect": {"morale": 6}
                },
                {
                    "id": "push",
                    "text": "Push through it",
                    "effect": {"morale": -5}
                }
            ]
        }
    ],

    "Redwood City": [
        {
            "id": "rc_server_outage",
            "name": "Server Outage",
            "description": "A production issue is getting worse. Ignoring it could get expensive.",
            "requires_input": True,
            "condition": {"bugs": {"min": 6}},
            "options": [
                {
                    "id": "fix",
                    "text": "Fix it now",
                    "effect": {"bugs": -6, "coffee": -12, "morale": -3}
                },
                {
                    "id": "delay_fix",
                    "text": "Delay and keep moving",
                    "effect": {"bugs": 8, "hype": -3}
                }
            ]
        },
        {
            "id": "rc_supplier_discount",
            "name": "Supplier Discount",
            "description": "A local supplier offers a limited-time deal on team essentials.",
            "requires_input": True,
            "options": [
                {
                    "id": "buy",
                    "text": "Buy supplies",
                    "effect": {"cash": -120, "coffee": 16, "morale": 3}
                },
                {
                    "id": "skip",
                    "text": "Save the cash",
                    "effect": {"morale": -1}
                }
            ]
        },
        {
            "id": "rc_customer_feedback",
            "name": "Brutal Customer Feedback",
            "description": "A potential user points out serious flaws. It hurts, but it could help.",
            "requires_input": True,
            "options": [
                {
                    "id": "accept",
                    "text": "Accept the criticism",
                    "effect": {"bugs": -3, "morale": -2}
                },
                {
                    "id": "dismiss",
                    "text": "Dismiss the feedback",
                    "effect": {"morale": 1, "hype": 2, "bugs": 2}
                }
            ]
        }
    ],

    "San Mateo": [
        {
            "id": "sm_burnout",
            "name": "Team Burnout",
            "description": "The team is running low on energy and patience.",
            "requires_input": True,
            "condition": {"morale": {"max": 55}},
            "options": [
                {
                    "id": "rest",
                    "text": "Force a rest day",
                    "effect": {"morale": 10, "coffee": 5, "cash": -80}
                },
                {
                    "id": "push",
                    "text": "Push through it",
                    "effect": {"morale": -12, "hype": 3}
                }
            ]
        },
        {
            "id": "sm_demo_day",
            "name": "Demo Day Invite",
            "description": "A local demo day could boost attention if you show up prepared.",
            "requires_input": True,
            "options": [
                {
                    "id": "present",
                    "text": "Present the product",
                    "effect": {"hype": 12, "cash": 200, "coffee": -5}
                },
                {
                    "id": "pass",
                    "text": "Pass and polish the product",
                    "effect": {"bugs": -2}
                }
            ]
        },
        {
            "id": "sm_team_dinner",
            "name": "Team Dinner",
            "description": "A shared meal could rebuild morale, but it costs money and time.",
            "requires_input": True,
            "options": [
                {
                    "id": "go",
                    "text": "Take the team out",
                    "effect": {"cash": -140, "morale": 8}
                },
                {
                    "id": "skip",
                    "text": "Stay focused on work",
                    "effect": {"coffee": 3, "morale": -4}
                }
            ]
        }
    ],

    "Burlingame": [
        {
            "id": "bu_airport_lead",
            "name": "Airport Investor Lead",
            "description": "You bump into a promising investor in transit.",
            "requires_input": True,
            "options": [
                {
                    "id": "chase",
                    "text": "Chase the lead",
                    "effect": {"cash": 350, "hype": 6, "coffee": -6}
                },
                {
                    "id": "ignore",
                    "text": "Ignore and stay disciplined",
                    "effect": {"bugs": -1}
                }
            ]
        },
        {
            "id": "bu_emergency_refill",
            "name": "Emergency Refill",
            "description": "A convenience stop could refill supplies before the final stretch.",
            "requires_input": True,
            "condition": {"coffee": {"max": 35}},
            "options": [
                {
                    "id": "refill",
                    "text": "Refill supplies",
                    "effect": {"cash": -90, "coffee": 20}
                },
                {
                    "id": "skip",
                    "text": "Risk it and move on",
                    "effect": {"morale": -3}
                }
            ]
        },
        {
            "id": "bu_press_tip",
            "name": "Press Tip-Off",
            "description": "A local blogger is looking for a startup story.",
            "requires_input": True,
            "options": [
                {
                    "id": "share",
                    "text": "Tell your story",
                    "effect": {"hype": 7, "morale": 2, "bugs": 1}
                },
                {
                    "id": "quiet",
                    "text": "Stay quiet until launch",
                    "effect": {"bugs": -1, "hype": -1}
                }
            ]
        }
    ],

    "San Bruno": [
        {
            "id": "sb_launch_prep",
            "name": "Launch Prep Sprint",
            "description": "The team can sprint toward launch, but it will cost energy and product stability.",
            "requires_input": True,
            "options": [
                {
                    "id": "sprint",
                    "text": "Sprint hard",
                    "effect": {"coffee": -12, "bugs": 4, "morale": -3}
                },
                {
                    "id": "steady",
                    "text": "Keep a steady pace",
                    "effect": {"morale": 2}
                }
            ]
        },
        {
            "id": "sb_press_ping",
            "name": "Local Press Ping",
            "description": "A reporter wants a quick comment before launch.",
            "requires_input": True,
            "options": [
                {
                    "id": "respond",
                    "text": "Respond quickly",
                    "effect": {"hype": 10, "coffee": -4}
                },
                {
                    "id": "ignore",
                    "text": "Ignore and stay focused",
                    "effect": {"bugs": -1}
                }
            ]
        },
        {
            "id": "sb_last_minute_bug",
            "name": "Last-Minute Bug Report",
            "description": "A serious issue appears at the worst possible time.",
            "requires_input": True,
            "condition": {"bugs": {"min": 3}},
            "options": [
                {
                    "id": "fix",
                    "text": "Fix it before launch",
                    "effect": {"bugs": -3, "coffee": -7, "morale": -1}
                },
                {
                    "id": "ship",
                    "text": "Ship anyway",
                    "effect": {"hype": 5, "bugs": 3, "morale": -4}
                }
            ]
        }
    ],

    "Daly City": [
        {
            "id": "dc_final_nerves",
            "name": "Final Stretch Nerves",
            "description": "Pressure rises as the destination gets close.",
            "requires_input": True,
            "api_condition": {
                "temperature": {"max": 50}
            },
            "options": [
                {
                    "id": "pep_talk",
                    "text": "Give a pep talk",
                    "effect": {"morale": 8, "coffee": -4}
                },
                {
                    "id": "push_forward",
                    "text": "Push harder",
                    "effect": {"morale": -6}
                }
            ]
        },
        {
            "id": "dc_supply_cache",
            "name": "Hidden Supply Cache",
            "description": "You find a stash of useful startup fuel.",
            "requires_input": True,
            "options": [
                {
                    "id": "take",
                    "text": "Take the supplies",
                    "effect": {"coffee": 15, "morale": 4}
                },
                {
                    "id": "leave",
                    "text": "Leave it and keep momentum",
                    "effect": {"hype": 2}
                }
            ]
        },
        {
            "id": "dc_big_bet",
            "name": "Final Marketing Push",
            "description": "You can spend heavily on one final push before arrival.",
            "requires_input": True,
            "condition": {"cash": {"min": 150}},
            "options": [
                {
                    "id": "invest",
                    "text": "Invest in the push",
                    "effect": {"cash": -150, "hype": 12, "morale": 2}
                },
                {
                    "id": "save",
                    "text": "Save the money",
                    "effect": {"morale": 1}
                }
            ]
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
    "San Jose": "Clear",
    "Santa Clara": "Sunny",
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
    "Clear": {"morale": 2,},
    "Sunny": {"morale": 2, "coffee": -2},
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