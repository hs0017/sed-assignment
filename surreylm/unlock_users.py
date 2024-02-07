import sys

sys.path.append("/Users/hollysherlock/PycharmProjects/sed-assignment")
from surreylm import db
from surreylm.database_models import User
from surreylm import create_app

app = create_app()


def unlock_users():
    """
    This function is used to unlock users who have been locked out of their account.
    :return: Returns nothing.
    """
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.locked:
                user.locked = False
                user.failed_login_attempts = 0
                db.session.commit()
                print("User " + str(user.email) + " has been unlocked.")


unlock_users()
