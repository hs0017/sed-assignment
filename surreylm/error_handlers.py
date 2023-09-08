# Purpose of this file: This file contains the error handlers for the License Management System.

# Importing the required modules.
from flask import render_template, Blueprint
from flask_login import current_user

errors = Blueprint('errors', __name__)  # Creating a blueprint for the error handlers.


@errors.app_errorhandler(500)
def internal_error(error):
    """
    This function is used to render the 500.html page when a 500 error occurs.
    :param error: The error that occurred.
    :return: Returns the 500.html page and the currently logged in user.
    """
    return render_template('500.html', user=current_user)


@errors.app_errorhandler(404)
def not_found_error(error):
    """
    This function is used to render the 404.html page when a 404 error occurs.
    :param error: The error that occurred.
    :return: Returns the 404.html page and the currently logged in user.
    """
    return render_template('404.html', user=current_user)


@errors.route('/500')
def error500():
    abort(500)
