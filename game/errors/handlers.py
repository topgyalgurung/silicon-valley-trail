from flask import render_template
from game.errors import errors_bp

@errors_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@errors_bp.app_errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500