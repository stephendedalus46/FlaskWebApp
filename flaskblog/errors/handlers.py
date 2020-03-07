from flask import Blueprint
from flask import render_template

errors = Blueprint('errors', __name__)

# there is also method errorhandler, but it would work only in that blueprint, not in entire app


@errors.app_errorhandler(404)  # error handlers are created similar to routes
def error_404(error):
    return render_template('errors/404.html'), 404  # need to add second value (number of error), by default is set to 200, which would be incorrect


@errors.app_errorhandler(403)  # error handlers are created similar to routes
def error_403(error):
    return render_template('errors/403.html'), 403  # need to add second value (number of error), by default is set to 200, which would be incorrect


@errors.app_errorhandler(500)  # error handlers are created similar to routes
def error_500(error):
    return render_template('errors/500.html'), 500  # need to add second value (number of error), by default is set to 200, which would be incorrect