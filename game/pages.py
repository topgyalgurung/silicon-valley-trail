import random
from flask import Blueprint, render_template, request, redirect 

from services.game_service import apply_action, calculate_event_outcome, save_game
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
        morale=100,
        coffee=50,
        hype=50,
        bugs=0,
        progress=0,
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

@game_routes.route("/move", methods=["GET","POST"])
def move():
    action = request.form["action"]
    game = get_latest_game()
    if action == "quit":
        reset_game()
        return redirect("/")
    elif action == "save":
        save_game(game)
        return redirect("/")
        db.session.commit()
        return render_template("pages/menu.html") # TODO: Save game to file
    else:
        game, event = apply_action(action, game)
        # return render_effect(result)
        event = None
        if game.current_event_key:
            city = game.current_location.city_name
            events = EVENTS_BY_LOCATION.get(city,[])
            event = next((e for e in events if e["key"] == game.current_event_key), None)
        return render_template("pages/event.html", game=game, event=event) # TODO: Apply action and return new game state

@game_routes.route('/event', methods=["POST"])
def handle_event():
    choice = request.form["choice"]
    game = get_latest_game()
    game = calculate_event_outcome(choice, game)
    return redirect('/game')