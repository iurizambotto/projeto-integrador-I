from flask import abort, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_manager

from app.extensions.database import db
from app.models.tables import Users

# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

def get_all_users():
    users = Users.query.order_by(Users.id).all() or []
    
    if len(users):
        json_users = [user.format() for user in users]
        return json_users
    else:
        abort(404)

def get_user(id): 
    user = Users.query.filter(Users.id == id).one_or_none() or None
    
    if user:
        return user.format()
    else:
        abort(404)

def add_user(form):
    content = {
        "username": form.username.data,
        "name": form.name.data,
        "email": form.email.data,
        "age": form.age.data
    }

    user = Users(**content)
    user.set_password(form.password.data)

    _commit_add(user)

    return user.format()

def _commit_add(user):
    db.session.add(user)
    db.session.commit()

def update_user(id):
    content = request.json
    print(content['name'])
    user = Users.query.filter(Users.id == id).one_or_none()
    print(user)
    user.name = content['name']
    db.session.commit()
    print(user.format())
    return jsonify({"User": user.format()})


def delete_user(id): 
    user = get_user(id)
    if user:
        user_deleted = user
        _delete_commit(user)
        return user_deleted.format()
    else:
        abort(404)

def _delete_commit(user):
    db.session.delete(user)
    db.session.commit()

def delete_all():
    users = get_all_users()
    
    users = [delete_user(user).format() for user in users]
    return users


def user_login(form):
    content = {
        "username": form.username.data
    }
    user = Users.query.filter(Users.username == form.username.data).one_or_none()

    if not user:
        abort(404)

    if user.check_password(form.password.data):
        user.authenticated = True
        _commit_add(user)
        login_user(user, remember=True)
        return True

def user_logout():
    user = current_user
    user.authenticated = False
    _commit_add(user)