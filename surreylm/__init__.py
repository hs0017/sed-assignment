from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "lmdatabase.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gdwjama bbawdjkwjdw'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .database_models import User, Software_owner, Vendor, Software

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('surreylm/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

    # with app.app_context():
    #    db.create_all()

    #  default_user = User(email='example@cat.com', first_name='Default', last_name='Admin', password='password',
    #                     admin=True)
    # db.session.add(default_user)
    # db.session.commit()
