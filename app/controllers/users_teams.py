from flask import abort, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_manager

from app.extensions.database import db
from app.models.tables import Users, UsersTeams

def get_users_team(manager_id):
    users_team = db.session.query(UsersTeams, Users).filter(
        manager_id == UsersTeams.manager_id,
        Users.id == UsersTeams.employee_id 
    ).all()
    return users_team
