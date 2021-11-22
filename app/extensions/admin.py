from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.extensions.database import db
from app.models.tables import Users, Task, Goal, UsersGoals, UsersTeams

def init_app(app):
    admin = Admin(app, name='API', template_mode='bootstrap3')
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Task, db.session))
    admin.add_view(ModelView(Goal, db.session))
    admin.add_view(ModelView(UsersGoals, db.session))
    admin.add_view(ModelView(UsersTeams, db.session))
