import random
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app
from jinja2 import TemplateNotFound
import requests

from game.services import (
    apply_action, 
    apply_current_event_choice, 
    save_game, 
    get_weather_by_city, 
    create_new_game, 
    reset_game
)
from game.extensions import db
from game.models import GameSession
from data.mock_api_data import ACTION_EFFECTS

game_routes = Blueprint("pages", __name__, template_folder="templates")

@game_routes.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@game_routes.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

@game_routes.app_errorhandler(TemplateNotFound)
def handle_template_not_found(e):
    return render_template('404.html'), 404

@game_routes.route("/")
def home():
    return render_template("pages/menu.html")

@game_routes.route("/new")
def new_game():
    """
    Returns a new game session or resets the current game session if it exists.
    """
    game = GameSession.query.first()
    if game:
        reset_game(game)
    else:
        game = create_new_game()
    return render_template("pages/intro.html", game_id=game.id)

@game_routes.route("/load")
def load_game():
    game = GameSession.query.order_by(GameSession.id.desc()).first()
    if not game:
        return redirect(url_for("pages.home"))
    return redirect(url_for("pages.show_game", game_id= game.id))

@game_routes.route("/game/<int:game_id>")
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
        weather_warning=weather_warning,
        game_id=game_id,
    )

@game_routes.route("/game/<int:game_id>/move", methods=["POST"])
def handle_move(game_id):
    ALLOWED_ACTIONS = ["travel", "rest", "work", "marketing", "save", "quit"]
    action = request.form.get("action")

    game = GameSession.query.get_or_404(game_id)
    
    if action == "quit":
        reset_game(game)
        return redirect(url_for("pages.home"))

    if action == "save":
        save_game(game)
        return redirect(url_for("pages.home"))
    
    # try:
    result = apply_action(action, game) 
    # except requests.exceptions.RequestException:
    #     return redirect(url_for("pages.show_game", game_id=game_id))
    # except Exception:
    #     current_app.logger.error("Error applying action: %s", action)
    #     abort(500, "Internal server error")

    if result.game_over:
        if result.status == "won":
            return render_template(
                "pages/game.html", 
                game=result.game,
                message=result.message,
                game_over=result.game_over,
                game_id=game_id,
            )
        else:
            return render_template(
                "pages/message.html",
                message=result.message,
                game_over=result.game_over,
                game_id=game_id,
            )
    if result.event:
        return render_template(
            "pages/event.html",
            game=game,
            event=result.event,
            message=result.message,
            action=action
        )

    message = ACTION_EFFECTS.get(action, {}).get("message")
    return render_template(
        "pages/event.html",
        game = game,
        event = None,
        message = message,
        game_over = result.game_over
    )


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

@game_routes.route("/quit")
def quit_game():
    return render_template("pages/message.html", message="Have a nice day!")