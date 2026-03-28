import random
from flask import Blueprint, render_template, request, redirect, url_for

from services.game_service import apply_action, apply_current_event_choice, save_game
from game.extensions import db
from game.models import GameSession, Location
from data.game_data import EVENTS_BY_LOCATION

game_routes = Blueprint("game", __name__)

def create_new_game():
    reset_game()
    start_location = Location.query.filter_by(city_name="San Jose").first()
    destination_location = Location.query.filter_by(city_name="San Francisco").first()
    # create fresh game session with initial state
    game = GameSession(
        current_day=1,
        current_location_id=start_location.id,
        destination_location_id=destination_location.id,
        status= "in_progress",
        cash=50000, 
        morale=100, # 0-100
        coffee=50, # if stays 0 for 2 turn -> lose
        hype=50,  # 0-100
        bugs=0,
        progress=0, # 0-100
        coffee_zero_turns=0,
        current_event_key=None,
    )
    db.session.add(game)
    db.session.commit()
    return game

def reset_game():
    GameSession.query.delete()
    db.session.commit()


def get_latest_game():
    latest_game = GameSession.query.order_by(GameSession.created_at.desc()).first()
    if not latest_game:
        return create_new_game()
    return latest_game 

@game_routes.route("/")
def home():
    return render_template("pages/menu.html")

@game_routes.route("/new", methods=["GET", "POST"])
def intro():
    create_new_game() # create new game in the database when user clicks new game 
    return render_template("pages/intro.html")

@game_routes.route("/game", methods=["GET", "POST"])
def show_game():
    game = get_latest_game() # get latest game session from the database or create a new one if none exists
    return render_template("pages/game.html", game=game)

@game_routes.route("/move", methods=["POST"])
def handle_move():
    action = request.form.get("action")
    game = get_latest_game()

    if action == "quit":
        reset_game()
        return redirect(url_for("game.home"))

    if action == "save":
        save_game(game)
        return redirect(url_for("game.home"))
    
    game, event = apply_action(action, game)

    if action == "travel" and event:
        return render_template("pages/event.html", game=game, event=event)
    return redirect(url_for("game.show_game"))

@game_routes.route('/event', methods=["POST"])
def handle_event():
    choice = request.form.get("choice")
    game=get_latest_game()
    game, message = apply_current_event_choice(choice, game)
    return render_template("pages/event.html", game=game, message = message, event=None)
