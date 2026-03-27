from flask import Blueprint, render_template
from flask import request

game_routes = Blueprint("game", __name__)

INITIAL_GAME_STATE = {
    "day": 1,
    "city": "San Jose",
    "location_detail": "San Jose is the capital of California",
    "weather": "Sunny",
    "team": {
        "money": 1000,
        "morale": 100,
        "coffee": 100,
        "hype": 100,
        "bugs": 0,
        "progress": 0,
    },
}

# def apply_action(action):

@game_routes.route("/")
def home():
    return render_template("pages/menu.html")

@game_routes.route("/new", methods=["POST"])
def intro():
    return render_template("pages/intro.html")

@game_routes.route("/show_game")
def show_game():
    return render_template("pages/game.html", game=INITIAL_GAME_STATE)

@game_routes.route("/move", methods=["POST"])
def move():
    action = request.form["action"]
    if action == "quit":
        # reset_game()
        return render_template("pages/menu.html") # TODO: Reset game to initial state
    elif action == "save":
        # save_game()
        return render_template("pages/menu.html") # TODO: Save game to file
    else:
        return render_template("pages/game.html", game=INITIAL_GAME_STATE) # TODO: Apply action and return new game state
        # result = apply_action(action)
        # return render_effect(result)