from flask import Blueprint, render_template
from copy import deepcopy
from data.mock_api_data import (
    INITIAL_GAME_STATE, LOCATIONS, EVENTS, MOCK_WEATHER, ACTION_EFFECTS
)
game_routes = Blueprint("pages", __name__, template_folder="templates")

@game_routes.route("/")
def home():
    return render_template("pages/menu.html")

@game_routes.route("/intro")
def intro():
    return render_template("pages/intro.html")

@game_bp.route("/new", methods=["POST"])
def start_new_game():
    return render_template("pages/intro.html")

