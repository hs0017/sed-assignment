# Purpose: This file contains the routes for the login and register pages.

# Importing the required modules.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .database_models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .validations import Validate
from . import create_app

auth = Blueprint('auth', __name__)  # Creating a blueprint for the auth routes.


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function is used to login the user.
    :return: Returns the login page and the currently logged in user.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and not user.locked:
            if check_password_hash(user.password, password):
                flash('Welcome to the License Management System!', category='success')
                login_user(user, remember=True)
                create_app().logger.info(f'{user.email} - Logged in successfully.')
                user.failed_login_attempts = 0
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect login details, please try again or contact your system administrator.',
                      category='error')
                create_app().logger.info(f'{user.email} - Invalid password entered.')
                user.failed_login_attempts += 1
                db.session.commit()
                if user.failed_login_attempts >= 3:
                    create_app().logger.info(f'{user.email} - Incorrect password attempts exceeded 3.'
                                             f'Account has been locked.')
                    user.locked = True
                    db.session.commit()
                    flash('Incorrect login details, please try again or contact your system administrator.',
                          category='error')
        else:
            if user and user.locked:
                create_app().logger.info(f'{email} - Account locked login attempt failed.')
                flash('Account has been locked, please contact your system administrator.',
                      category='error')
            else:
                create_app().logger.info(f'{email} - Invalid email login attempt failed.')
                flash('Incorrect login details, please try again or contact your system administrator.',
                      category='error')

    return render_template("login.html", user=current_user)


@auth.route('/register', methods=['GET', 'POST'])
def sign_up():
    """
    This function is used to register the user.
    :return: Returns the register page and the currently logged in user.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        people_name_valid = Validate.people_name(first_name, last_name)
        password_valid = Validate.password(password1, password2, first_name, last_name)
        email_valid = Validate.email(email)

        if user:
            flash('Email already exists.', category='error')
        elif not email_valid or not password_valid or not people_name_valid:
            return render_template("register.html", user=current_user)
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name,
                            password=generate_password_hash(password1, method='sha512'))
            db.session.add(new_user)
            db.session.commit()
            create_app().logger.info(f'{email} - Account created.')
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("register.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    This function is used to logout the user.
    :return: Returns a redirect to the login page.
    """
    create_app().logger.info(f'{current_user.email} - Logged out.')
    logout_user()
    return redirect(url_for('auth.login'))
