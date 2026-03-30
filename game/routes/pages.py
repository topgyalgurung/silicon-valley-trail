import requests
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app
from game.services import (
    apply_action, 
    apply_current_event_choice, 
    save_game, 
    get_weather_by_city, 
    create_new_game, 
    reset_game
)
from game.models import GameSession
from data.mock_api_data import ACTION_EFFECTS
from game.utils import get_game_weather, calculate_progress

game_routes = Blueprint("pages", __name__, template_folder="templates")

ALLOWED_ACTIONS = ["travel", "rest", "work", "marketing", "save", "quit"]

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
    weather_data, weather_warning = get_game_weather(game)

    days_left = max(0, 20 - game.current_day)
    return render_template(
        "pages/game.html", 
        game=game, 
        progress=game.progress,
        days_left=days_left,
        weather_data=weather_data,
        weather_warning=weather_warning,
        game_id=game_id,
    )

@game_routes.route("/game/<int:game_id>/move", methods=["POST"])
def handle_move(game_id):
    action = request.form.get("action")

    if action not in ALLOWED_ACTIONS:
        abort(400, "Invalid action")

    # Load the current game session from the database or return 404 if not found
    game = GameSession.query.get_or_404(game_id)
    
    if action in {"quit", "save"}:
        save_game(game)
        return redirect(url_for("pages.home"))
    
    try:
        result = apply_action(action, game) 
    except requests.exceptions.RequestException:
        return redirect(url_for("pages.show_game", game_id=game_id))
    except Exception:
        current_app.logger.exception("Error applying action: %s", action)
        abort(500, "Internal server error")

    if result.game_over:
        # template = "pages/game.html" if result.status == "won" else "pages/message.html"
        return render_template(
            "pages/message.html", 
            game=result.game, 
            message=result.message, 
            game_over=result.game_over, 
            game_id=game_id
        )
    if result.event:
        return render_template(
            "pages/event.html", 
            game=result.game,
            event=result.event,
            message=result.message,
            action=action
        )

    # display message for other actions except travel
    message = ACTION_EFFECTS.get(action, {}).get("message")
    return render_template(
        "pages/message.html",
        game = game,
        event = None,
        message = message
    )


@game_routes.route('/game/<int:game_id>/event', methods=["POST"])
def handle_event(game_id):
    choice = request.form.get("choice")
    if not choice:
        abort(400, "Invalid choice")

    game = GameSession.query.get_or_404(game_id)
    game, message = apply_current_event_choice(choice, game)
    save_game(game)
    days_left = max(0, 20 - game.current_day)
    weather_data, weather_warning = get_game_weather(game)
    return render_template(
        "pages/game.html", 
        game=game, 
        message = message, 
        event=None,
        days_left=days_left,
        weather_data=weather_data,
        weather_warning=weather_warning,
        progress=game.progress
    )

@game_routes.route("/quit")
def quit_game():
    return render_template("pages/message.html", message="Have a nice day!")