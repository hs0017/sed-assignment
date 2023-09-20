# Purpose: This file is the main file for the surreylm package. It is used to create the flask app and the database.

# Importing the required modules.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "lmdatabase.db"


def create_app(database_uri='sqlite:///lmdatabase.db'):
    """
    This function is used to create the flask app and the database.
    :return: Returns the flask app.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gdwjama bbawdjkwjdw'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .error_handlers import errors

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(errors)

    from .database_models import User, Software_owner, Vendor, Software

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """
        This function is used to reload the user object from the user ID stored in the session.
        :param id: The user ID.
        :return: Returns the user object.
        """
        return User.query.get(int(id))
    return app


def create_database(app):
    """
    This function is used to create the database if it doesn't exist.
    :param app: The flask app.
    """
    if not path.exists('surreylm/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
