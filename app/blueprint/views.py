from datetime import datetime, timedelta
from flask.helpers import url_for
from app.forms.login_form import LoginForm
from app.extensions.database import db
from flask import request, jsonify, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.tables import Users, Goal, Task
from app.forms.login_form import LoginForm
from app.forms.create_user_form import CreateUserForm
from app.forms.create_goal_form import CreateGoalForm
from app.forms.create_task_form import CreateTaskForm
from app.controllers.users import *

# TESTE

def init_app(app):
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    @app.route('/api/login/', methods=["GET", "POST"])
    @app.route('/api/', methods=["GET", "POST"])
    @app.route('/', methods=["GET", "POST"])
    def get_login():
        print("login", current_user.is_authenticated())
        if not current_user.is_authenticated():
            form = LoginForm()
            print(form.validate_on_submit())
            if form.validate_on_submit():
                print(form.validate_on_submit())
                if user_login(form):
                    flash('Logado com {}'.format(
                        form.username.data))
                    return redirect(url_for('homepage'))

                else:
                    flash('Usuário ou senha inválidos')
        else:
            return redirect(url_for('get_login'))

        return render_template('login.html', title='Entrar', form=form)

    @app.route('/api/logout')
    @login_required
    def get_logout():
        logout_user
        user_logout()
        return redirect(url_for('get_login'))

    @app.route('/api/user/', methods=['GET', 'POST'])
    def create_user():
        form = CreateUserForm()
        print(form)
        if form.validate_on_submit():
            try:
                user = Users.query.filter(Users.username == form.username.data).one_or_none() or None
                if not user:
                    user = add_user(form)
                    # return redirect(url_for('#'))
                    return redirect(url_for('get_login'))
                else:
                    flash('Este usuário já existe')
            except Exception as e:
                print(e)
        
        return render_template('create_user.html', title='Criar usuário', form=form)

    @app.route('/api/my_profile/', methods=['GET', 'POST'])
    @login_required
    def my_profile():

        if not current_user.is_authenticated():
            abort(401)
        
        return render_template("user.html", user=current_user)
    # @app.route('/api/users/', methods=['GET'])
    # @login_required
    # def get_users():
    #     if not current_user.is_authenticated():
    #         abort(401)
        
    #     users = get_all_users()
    #     if len(users) == 0:
    #         abort(404)
            
    #     return render_template("users.html", users=users)

    @app.route('/api/home/', methods=['GET', 'POST'])
    @login_required
    def homepage():
        current_task = db.session.query(Task, Users).filter(
                Task.user_id == current_user.id,
                Task.achieved == False,
                Task.user_id == Users.id,
            ).order_by(Task.created_at.desc()).limit(1)

        return render_template('home.html', title='Página inicial', current_task=current_task)

    
    @app.route('/api/atividades/concluidas/', methods=['GET', 'POST'])
    @app.route('/api/atividades/', methods=['GET', 'POST'])
    @login_required
    def atividades():
        achieved = False
        print(request.url)
        if 'concluidas' in request.url:
            achieved = True
        
        tasks = db.session.query(Task, Users).filter(
                Task.user_id == current_user.id,
                Task.achieved == achieved,
                Task.user_id == Users.id,
            ).order_by(Task.id.desc()).limit(6)

        return render_template('atividades.html', tasks=tasks, url=request.url)

    @app.route('/api/atividade/<int:id>', methods=['GET', 'POST'])
    @login_required
    def atividade(id):
        tasks = db.session.query(Task, Users).filter(
                Task.id == id,
                Task.user_id == current_user.id,
                Task.achieved == False,
                Task.user_id == Users.id,
            ).limit(1)

        return render_template('atividade.html', tasks=tasks)

    @app.route('/api/atividade/<int:id>/deletar', methods=['DELETE', 'POST', 'GET'])
    def delete_task(id):
        task = Task.query.filter(Task.id == id).one_or_none() or None

        db.session.delete(task)
        db.session.commit()

        return redirect(url_for('atividades'))

    @app.route('/api/metas/', methods=['GET', 'POST'])
    @login_required
    def metas():
        form = CreateGoalForm()
        if form.validate_on_submit():
            goal_content = {
                "name": form.name.data,
                "description": form.description.data,
                "created_by": current_user.id,
                "created_at": datetime.now(),
                "achieved": False
            }

            goal = Goal(**goal_content)
            _commit_add(goal)
        goals = Goal.query.order_by(Goal.id.desc()).limit(6)
        print(request.json)
        if request.form.get('achieved'):
            goal.achieved = True
            _commit_add(goal)

        return render_template('metas.html')
    
    @app.route('/api/relatorios/', methods=['GET', 'POST'])
    @login_required
    def relatorios():

        return render_template('relatorios.html')

    @app.route('/api/task/', methods=['GET', 'POST'])
    def create_task():
        form = CreateTaskForm()
        form.user_id.choices = [(g.id, g.name) for g in Users.query.order_by('name')]
        print(form)
        if form.validate_on_submit():
            print(form)
            task_content = {
                "name": form.name.data,
                "description": form.description.data,
                "user_id": form.user_id.data,
                "created_by": current_user.id,
                "created_at": datetime.now(),
                "achieved": False
            }

            task = Task(**task_content)
            _commit_add(task)
            return redirect(url_for('atividades'))

        return render_template('criar_atividade.html', form=form)

    
    def _commit_add(user):
        db.session.add(user)
        db.session.commit()

    # @app.route('/api/users/<int:id>', methods=['PATCH'])
    # def update_user(id):
    #     content = request.json
    #     print(content['name'])
    #     user = Users.query.filter(Users.id == id).one_or_none()
    #     print(user)
    #     user.name = content['name']
    #     db.session.commit()
    #     print(user.format())
    #     return jsonify({"User": user.format()})


    # @app.route('/api/users/all/', methods=['DELETE'])
    # def delete_all():
    #     users = Users.query.order_by(Users.id).all()

    #     if len(users) == 0:
    #         abort(404)
        
    #     users = delete_all()

    #     return jsonify({
    #         'success': True,
    #         'users': users
    #     })

    # @app.route('/api/users/<int:id>', methods=['DELETE'])
    # def delete_user(id): 
        
    #     user = delete_user(id)

    #     if not user:
    #         abort(404)
            
    #     return jsonify({
    #         'success': True,
    #         'user': user
    #     })

