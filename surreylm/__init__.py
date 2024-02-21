# Purpose: This file is the main file for the surreylm package. It is used to create the flask app and the database.

# Importing the required modules.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
import logging

db = SQLAlchemy()
DB_NAME = "surreylm-mysqldb"
db_username = os.environ["db_username"]
db_password = os.environ["db_password"]
ca_cert = os.environ["ca_cert"]


def create_app(database_uri=f'mysql+mysqlconnector://{db_username}:{db_password}@surreylm-db.mysql.database.azure.com:3306/{DB_NAME}?ssl_ca={ca_cert}&ssl_mode=REQUIRED'):
    """
    This function is used to create the flask app and the database.
    :return: Returns the flask app.
    """
    logging.basicConfig(filename='record.log',
                        level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ["secret_key"]
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


#def create_database(app):
#    """
#    This function is used to create the database if it doesn't exist.
#    :param app: The flask app.
#    """
#    if not path.exists('surreylm/' + DB_NAME):
#        db.create_all(app=app)
#        print('Created Database!')
