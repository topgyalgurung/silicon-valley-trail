from flask import Blueprint

errors_bp = Blueprint('errors', __name__)

from game.errors import handlers