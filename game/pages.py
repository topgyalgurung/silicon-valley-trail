import random
from flask import Blueprint, render_template, request, redirect, url_for

from services.game_service import apply_action, apply_current_event_choice, save_game
from services.weather_service import get_weather_by_city
from game.extensions import db
from game.models import GameSession
from game.helpers import create_new_game

# TODO: rate limit the game routes 


game_routes = Blueprint("game", __name__)


@game_routes.route("/")
def home():
    return render_template("pages/menu.html")

@game_routes.route("/new", methods=["GET", "POST"])
def intro():
    if request.method == "POST":
        game = create_new_game()
        return render_template("pages/intro.html", game_id=game.id)
    return render_template("pages/intro.html")

@game_routes.route("/game/<int:game_id>", methods=["GET", "POST"])
def show_game(game_id):
    game = GameSession.query.get_or_404(game_id) # get latest game session from the database or create a new one if none exists
    weather_data = get_weather_by_city(game.current_location.city_name)
    return render_template(
        "pages/game.html", 
        game=game, 
        weather_data=weather_data,
        game_id=game_id
    )

@game_routes.route("/game/<int:game_id>/move", methods=["POST"])
def handle_move(game_id):
    game = GameSession.query.get_or_404(game_id)
    action = request.form.get("action")

    if action == "quit":
        # reset_game()
        return redirect(url_for("game.home"))

    if action == "save":
        save_game(game)
        return redirect(url_for("game.home"))
    
    game, event = apply_action(action, game)

    if action == "travel" and event:
        return render_template(
            "pages/event.html", 
            game=game, 
            event=event
        )
    return redirect(url_for("game.show_game", game_id=game.id))

@game_routes.route('/game/<int:game_id>/event', methods=["POST"])
def handle_event(game_id):
    choice = request.form.get("choice")
    game = GameSession.query.get_or_404(game_id)
    game, message = apply_current_event_choice(choice, game)
    return render_template(
        "pages/event.html", 
        game=game, 
        message = message, 
        event=None
    )
