import requests
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, flash
from game.services import (
    apply_action, 
    apply_current_event_choice, 
)
from game.models import GameSession
from game.utils.utils import get_game_weather
from game.utils.state import save_game, create_new_game, clear_all_games
from data.mock_api_data import ACTION_EFFECTS

game_routes = Blueprint("game", __name__, url_prefix="") # api/v1

ALLOWED_ACTIONS = ["travel", "rest", "work", "marketing", "save", "quit"]

# todo: POST -> redirect -> GET pattern

def render_game_page(game, message=None):
    days_left = max(0, 21 - game.current_day)
    weather_data, weather_warning = get_game_weather(game)
    return render_template(
        "pages/game.html", 
        game=game, 
        message=message,
        progress=game.progress,
        days_left=days_left,
        weather_data=weather_data,
        weather_warning=weather_warning,
        game_id=game.id,
    )


@game_routes.route("/")
def home():
    return render_template("pages/menu.html")

@game_routes.route("/new")
def new_game():
    clear_all_games()
    game = create_new_game()
    return render_template("pages/intro.html", game_id=game.id)

@game_routes.route("/load")
def load_game():
    game = GameSession.query.order_by(GameSession.id.desc()).first()
    if not game:
        return redirect(url_for("game.home"))
    return render_game_page(game,"✅ Game loaded successfully" )

@game_routes.route("/game/<int:game_id>")
def show_game(game_id):
    game = GameSession.query.get_or_404(game_id) # get latest game session from the database or create a new one if none exists
    message = request.args.get("message")
    return render_game_page(game, message)

@game_routes.route("/game/<int:game_id>/move", methods=["POST"])
def handle_move(game_id):
    action = request.form.get("action")

    if action not in ALLOWED_ACTIONS:
        abort(400, "Invalid action")

    # Load the current game session from the database or return 404 if not found
    game = GameSession.query.get_or_404(game_id)

    if action == "save":
        save_game(game)
        return render_game_page(game, "💾 Game saved successfully.")
    
    if action == "quit":
        save_game(game)
        return redirect(url_for("game.home"))
    
    try:
        result = apply_action(action, game) 
    except requests.exceptions.RequestException:
        return redirect(url_for("game.show_game", game_id=game_id))
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
    return render_game_page(game, message)
    # return render_template(
    #     "pages/game.html",
    #     game = game,
    #     event = None,
    #     message = message
    # )

@game_routes.route('/game/<int:game_id>/event', methods=["POST"])
def handle_event(game_id):
    choice = request.form.get("choice")
    if not choice:
        abort(400, "Invalid choice")

    game = GameSession.query.get_or_404(game_id)
    game, message = apply_current_event_choice(choice, game)
    save_game(game)
    return render_game_page(game)

@game_routes.route("/quit")
def quit_game():
    return render_template("pages/message.html", message="Have a nice day!")

@game_routes.route("/test-500")
def test_500():
    raise Exception("Test 500 error")
