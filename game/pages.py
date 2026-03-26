from flask import Blueprint, render_template

game_routes = Blueprint("pages", __name__)

@game_routes.route("/")
def home():
    return render_template("pages/menu.html")

@game_routes.route("/start")
def menu():
    return render_template("pages/new-game.html")

