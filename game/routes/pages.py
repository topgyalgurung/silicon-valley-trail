import random
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from jinja2 import TemplateNotFound
import requests

from game.services import apply_action, apply_current_event_choice, save_game, get_weather_by_city, create_new_game, reset_game
from game.extensions import db
from game.models import GameSession
from data.mock_api_data import ACTION_EFFECTS
# TODO: rate limit the game routes 

game_routes = Blueprint("pages", __name__, template_folder="templates")

@game_routes.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@game_routes.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@game_routes.route("/")
def home():
    try:
        return render_template("pages/menu.html")
    except TemplateNotFound:
        abort(404)

@game_routes.route("/new", methods=["POST"])
def new_game():
    game = GameSession.query.first()
    if game:
        reset_game(game)
    game = create_new_game()
    return render_template("pages/intro.html", game_id=game.id)

@game_routes.route("/load", methods=["POST"])
def load_game():
    game = GameSession.query.order_by(GameSession.id.desc()).first()
    if not game:
        return redirect(url_for("pages.home"))
    return redirect(url_for("pages.show_game", game_id= game.id))

@game_routes.route("/game/<int:game_id>", methods=["GET", "POST"])
def show_game(game_id):
    game = GameSession.query.get_or_404(game_id) # get latest game session from the database or create a new one if none exists
    weather_data = get_weather_by_city(game.current_location.city_name)

    weather_warning = None
    if not weather_data["ok"]:
        weather_warning = "live weather unavailable. Showing fallback data."
    return render_template(
        "pages/game.html", 
        game=game, 
        weather_data=weather_data,
        game_id=game_id,
    )

@game_routes.route("/game/<int:game_id>/move", methods=["POST"])
def handle_move(game_id):
    try:
        game = GameSession.query.get_or_404(game_id)
    except:
        return {"message": "Game not found"}
    action = request.form.get("action")
    
    if action == "quit":
        reset_game(game)
        return redirect(url_for("pages.home"))

    if action == "save":
        save_game(game)
        return redirect(url_for("pages.home"))
    
    try:
        game, event = apply_action(action, game, message=None)
    except requests.exceptions.RequestException:
        return redirect(url_for("pages.show_game", game_id=game_id))
    except Exception:
        game_routes.logger.error("Error applying action: %s", action)

    if action == "travel" and event:
        return render_template(
            "pages/event.html", 
            game=game, 
            event=event
        )
    message = ACTION_EFFECTS.get(action, {}).get("message")
    return render_template("pages/event.html", game=game, message=message)

@game_routes.route('/game/<int:game_id>/event', methods=["GET", "POST"])
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

@game_routes.route('/messages/<int:idx>')
def message(idx):
    game_routes.logger.info(f"Rendering message {idx}")
    messages = ['Message Zero', 'Message One', 'Message Two']
    try:
        game_routes.logger.debug('Get message with index:{}'.format(idx))
        return render_template('pages/message.html', message=messages[idx])
    except IndexError:
        game_routes.logger.error('Index {} is causing an :{}'.format(idx))
        abort(404)