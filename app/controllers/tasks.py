from flask import abort

from app.models.tables import Task

# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

def get_all_tasks():
    tasks = Task.query.order_by(Task.id).all() or []
    
    if len(tasks):
        json_tasks = [task for task in tasks]
        return json_tasks
    else:
        abort(404)

def get_task(id):
    task = Task.query.filter(Task.id == id).one_or_none() or None
    
    if task:
        return task
    else:
        abort(404)
