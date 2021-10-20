from datetime import timedelta
from flask import session
from flask_login import LoginManager
from app.models.tables import Users

login_manager = LoginManager()
login_manager.login_view = 'get_login'

def init_app(app):
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        """Given *user_id*, return the associated User object.

        :param unicode user_id: user_id (id) user to retrieve

        """
        return Users.query.get(int(id))

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=10)
