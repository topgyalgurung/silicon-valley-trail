import random
from data.mock_api_data import EVENTS_BY_LOCATION

## currently not being implemented
def event_is_allowed(game, event):
    """Return True if event is allowed based on game state"""
    condition = event.get("condition", {})
    bugs_rule = condition.get("bugs", {})
    if bugs_rule:
        if game.bugs < bugs_rule.get("min", 0):
            return False
    return True
