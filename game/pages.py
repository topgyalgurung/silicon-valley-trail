from flask import Blueprint, render_template, request 
from game.extensions import db
from game.models import GameSession
from data.seed_data import INITIAL_GAME_STATE

game_routes = Blueprint("game", __name__)

def create_new_game():
    game = GameSession(
        day=INITIAL_GAME_STATE["day"],
        city=INITIAL_GAME_STATE["city"],
        current_location_detail=INITIAL_GAME_STATE["current_location_detail"],
        money=INITIAL_GAME_STATE["money"],
        morale=INITIAL_GAME_STATE["morale"],
        coffee=INITIAL_GAME_STATE["coffee"],
        hype=INITIAL_GAME_STATE["hype"],
        bugs=INITIAL_GAME_STATE["bugs"],
        progress=INITIAL_GAME_STATE["progress"],
    )
    db.session.add(game)
    db.session.commit()
    return game

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
    