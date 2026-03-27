from flask import Blueprint, render_template, request 
from game.extensions import db
from game.models import GameSession, Location

game_routes = Blueprint("game", __name__)

def create_new_game():
    start_location = Location.query.filter_by(city_name="San Jose").first()
    destination_location = Location.query.filter_by(city_name="San Francisco").first()
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

# def apply_action(action):

@game_routes.route("/")
def home():
    return render_template("pages/menu.html")

@game_routes.route("/new", methods=["POST"])
def intro():
    create_new_game() # create new game in the database when user clicks new game 
    return render_template("pages/intro.html")

@game_routes.route("/show_game")
def show_game():
    game = get_latest_game()
    return render_template("pages/game.html", game=game)

@game_routes.route("/move", methods=["POST"])
def move():
    action = request.form["action"]
    game = get_latest_game()
    if action == "quit":
        # reset_game()
        return render_template("pages/menu.html") # TODO: Reset game to initial state
    elif action == "save":
        db.session.commit()
        return render_template("pages/menu.html") # TODO: Save game to file
    else:
        # apply_action(action)
        # return render_effect(result)
        db.session.commit()
        return render_template("pages/game.html", game=game) # TODO: Apply action and return new game state
    