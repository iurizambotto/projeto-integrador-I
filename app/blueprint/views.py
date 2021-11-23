from datetime import datetime, timedelta
from flask.helpers import url_for
from app.forms.login_form import LoginForm
from app.extensions.database import db
from flask import request, jsonify, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.tables import Users, Goal, Task, UsersTeams, UsersGoals
from app.forms.login_form import LoginForm
from app.forms.create_user_form import CreateUserForm
from app.forms.create_goal_form import CreateGoalForm
from app.forms.create_task_form import CreateTaskForm
from app.forms.edit_task_form import EditTaskForm
from app.forms.create_new_relationship_form import CreateNewRelationshipForm
from app.controllers.users import *
from app.controllers.tasks import *
from app.controllers.users_teams import *

# Teste

def init_app(app):
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
    @app.route('/api/login/', methods=["GET", "POST"])
    @app.route('/api/', methods=["GET", "POST"])
    @app.route('/', methods=["GET", "POST"])
    def get_login():
        try:
            if not current_user.is_authenticated():
                form = LoginForm()

                if form.validate_on_submit():

                    if user_login(form):
                        flash('Logado com {}'.format(
                            form.email.data))
                        return redirect(url_for('homepage'))

                    else:
                        flash('Usuário ou senha inválidos')
            else:
                return redirect(url_for('get_login'))
        except:
            if not current_user.is_authenticated:
                form = LoginForm()
                print(form.validate_on_submit())
                if form.validate_on_submit():
                    print(form.validate_on_submit())
                    if user_login(form):
                        flash('Logado com {}'.format(
                            form.email.data))
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
                user = Users.query.filter(Users.email == form.email.data).one_or_none() or None
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

        current_goal = db.session.query(Goal, UsersGoals, Users, UsersTeams).filter(
                Goal.id == UsersGoals.goal_id,
                Goal.achieved == False,
                UsersTeams.manager_id == current_user.id,
                UsersGoals.user_id == Users.id,
            ).order_by(Goal.created_at.desc()).limit(1)

        tasks_pending = db.session.query(Task, Users).filter(
                Task.user_id == current_user.id,
                Task.achieved == False,
                Task.user_id == Users.id,
            ).order_by(Task.created_at.desc()).count()

        achieved_today = db.session.query(Task, Users).filter(
                Task.user_id == current_user.id,
                Task.achieved == True,
                Task.achieved_at >= datetime.today().strftime("%Y-%m-%d"),
                Task.user_id == Users.id,
            ).order_by(Task.created_at.desc()).count()
        
        return render_template(
            'home.html',
            title='Página inicial',
            current_task=current_task,
            current_goal=current_goal,
            tasks_pending=tasks_pending,
            achieved_today=achieved_today,
        )

    @app.route('/api/atividades/concluidas/', methods=['GET', 'POST'])
    @app.route('/api/atividades/', methods=['GET', 'POST'])
    @login_required
    def atividades():
        achieved = False

        if 'concluidas' in request.url:
            achieved = True
        
        tasks = db.session \
            .query(Task, Users, Goal) \
            .filter(
                Task.user_id == current_user.id,
                Task.achieved == achieved,
                Task.user_id == Users.id
            ) \
            .filter(
                (Task.goal_id == Goal.id)
            ) \
            .order_by(Task.id.desc()) \
            .distinct() \
            .limit(6)

        print(tasks)
        return render_template('atividades.html', tasks=tasks, url=request.url)

    @app.route('/api/task/', methods=['GET', 'POST'])
    @login_required
    def create_task():
        form = CreateTaskForm()
        form.user_id.choices = [(g.id, g.name) for g in Users.query.order_by('name')]

        users = get_users_team(current_user.id)
        users_id = [user.id for user_team, user in users]
        users_goals = db.session.query(UsersGoals, Goal).filter(
            Goal.id == UsersGoals.goal_id
        ).filter(UsersGoals.user_id.in_(users_id)).all()

        form.goal_id.choices = list(set((goal.id, goal.name) for user_goal, goal in users_goals))
        print(form.goal_id.choices)

        if form.validate_on_submit():

            task_content = {
                "name": form.name.data,
                "description": form.description.data,
                "user_id": form.user_id.data,
                "goal_id": form.goal_id.data,
                "created_by": current_user.id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "achieved": False
            }

            task = Task(**task_content)
            _commit_add(task)
            return redirect(url_for('atividades'))

        return render_template('criar_atividade.html', form=form)

    @app.route('/api/atividade/<int:id>', methods=['GET', 'POST'])
    @login_required
    def atividade(id):
        tasks = db.session.query(Task, Users).filter(
                Task.id == id,
                Task.user_id == current_user.id,
                Task.user_id == Users.id,
            ).limit(1)

        return render_template('atividade.html', tasks=tasks)


    @app.route('/api/atividade/<int:id>/editar', methods=['GET', 'POST'])
    @login_required
    def edit_task(id):
        tasks = db.session.query(Task, Users).filter(
                Task.id == id,
            ).limit(1)
        
        task = get_task([task.id for task, user in tasks][0])
        
        form = EditTaskForm()

        form.user_id.choices = [(current_user.id, current_user.name)]
        users = get_users_team(current_user.id)
        form.user_id.choices += [(user.id, user.name) for user_team, user in users]
        form.achieved.choices = [(0, "Não"), (1, "Sim")]

        users = get_users_team(current_user.id)
        users_id = [user.id for user_team, user in users]
        users_goals = db.session.query(UsersGoals, Goal).filter(
            Goal.id == UsersGoals.goal_id
        ).filter(UsersGoals.user_id.in_(users_id)).all()

        form.goal_id.choices = list(set((goal.id, goal.name) for user_goal, goal in users_goals))
        print(form.goal_id.choices)

        if form.validate_on_submit():
            print(form.data)
            task.name = form.name.data
            task.description = form.description.data
            task.user_id = form.user_id.data
            task.achieved = bool(form.achieved.data)
            task.updated_at = datetime.now()

            if task.achieved:
                task.achieved_at = datetime.now()

            db.session.commit()
            print(task.id, task.name, task.description, task.achieved, task.format())
            return redirect(url_for('atividades'))

        return render_template('editar_atividade.html', form=form, tasks=tasks)

    @app.route('/api/atividade/<int:id>/deletar', methods=['DELETE', 'POST', 'GET'])
    @login_required
    def delete_task(id):
        task = Task.query.filter(Task.id == id).one_or_none() or None

        db.session.delete(task)
        db.session.commit()

        return redirect(url_for('atividades'))
    
    @app.route('/api/metas/concluidas/', methods=['GET', 'POST'])
    @app.route('/api/metas/', methods=['GET', 'POST'])
    @login_required
    def metas():
        achieved = False

        if 'concluidas' in request.url:
            achieved = True
    
        # SEPARAR SE OS CARAS SAO GESTORES OU NAO PARA FILTRAR AS METAS DE CADA UM (GESTOR VE DO TIME TODO)
        users_team = db.session.query(UsersTeams).filter(
                UsersTeams.manager_id == current_user.id,
            )
        is_manager = [userteam.id for userteam in users_team]

        if is_manager:
            # PEGA TODAS GOALS DO TIME
            team_users = [current_user.id]+ [user_team.employee_id for user_team in users_team]
            print(team_users)
            goals = db.session.query(Goal, UsersGoals, Users, UsersTeams).filter(
                            Goal.id == UsersGoals.goal_id,
                            Goal.achieved == achieved,
                            UsersGoals.user_id.in_(team_users),
                        ).with_entities(Goal.id, Goal.name, Goal.description, Goal.achieved, Users.name).order_by(Goal.created_at.desc()).distinct().limit(6)

        else:
            # PEGA SÓ AS GOALS DO USUÁRIO
            goals = db.session.query(Goal, UsersGoals, Users, UsersTeams).filter(
                            Goal.id == UsersGoals.goal_id,
                            Goal.achieved == achieved,
                            UsersGoals.user_id == Users.id,
                        ).order_by(Goal.created_at.desc()).distinct().limit(6)
        print(goals)
        # goals = db.session.query(Goal) \
        #     .filter(
        #         Goal.achieved == achieved,
        #     ) \
        #     .order_by(Goal.id.desc()) \
        #     .limit(6)

        return render_template('metas.html', goals=goals, url=request.url)


    @login_required
    @app.route('/api/metas/', methods=['GET', 'POST'])
    def create_goal():
        print(request.method)
        if request.method == 'POST':
            print("forms", request.form.getlist("users"))

        form = CreateGoalForm()
        users = get_users_team(current_user.id)

        form.users.choices = [(user.id, user.name) for user_team, user in users]
        
        print(form.validate(), form.data, form.errors, form.submit())
        if form.validate_on_submit():

            goal_content = {
                "name": form.name.data,
                "description": form.description.data,
                "created_by": current_user.id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "achieved": False
            }

            goal = Goal(**goal_content)
            _commit_add(goal)
            
            for user_id in form.data['users']:
                users_goal_content = {
                    "goal_id": goal.id,
                    "user_id": user_id,
                    "created_by": current_user.id,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
                users_goal = UsersGoals(**users_goal_content)
                _commit_add(users_goal)

            return redirect(url_for('metas'))

        return render_template('criar_meta.html', form=form)

    @app.route('/api/meta/<int:id>', methods=['GET', 'POST'])
    @login_required
    def view_goal(id):
        goal = db.session.query(Goal, Users).filter(
                Goal.id == id,
            ).limit(1)

        return render_template('meta.html', goals=goal)

    @app.route('/api/meta/<int:id>/editar', methods=['GET', 'POST'])
    @login_required
    def edit_goal(id):
        goals = db.session.query(Goal, Users).filter(
                Task.id == id,
            ).limit(1)
        
        # goal = get_task([goal.id for goal, user in goals][0])


    @app.route('/api/meta/<int:id>/deletar', methods=['DELETE', 'POST', 'GET'])
    @login_required
    def delete_goal(id):
        goal = Goal.query.filter(Goal.id == id).one_or_none() or None

        db.session.delete(goal)
        db.session.commit()

        return redirect(url_for('metas'))

    @app.route('/api/relatorios/', methods=['GET', 'POST'])
    @login_required
    def relatorios():

        return render_template('relatorios.html')

    @app.route('/api/my_team/', methods=['GET', 'POST'])
    @login_required
    def my_team():
        users = get_users_team(current_user.id)

        return render_template("team.html", users=users)
    
    @app.route('/api/relationship/', methods=['GET', 'POST'])
    def create_new_relationship():
        form = CreateNewRelationshipForm()

        users = db.session.execute("""
        SELECT users.id, users.name
        FROM users
        LEFT JOIN users_team on users_team.employee_id = users.id
        WHERE users."function" = 0 AND users_team.employee_id is null
        ORDER BY users.name
        """)
        
        form.user_id.choices = [(id, name) for id, name in users]

        if form.validate_on_submit():
            print(form)
            user_team_content = {
                "manager_id": current_user.id,
                "employee_id": form.user_id.data,
                "created_by": current_user.id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }

            user_team = UsersTeams(**user_team_content)
            _commit_add(user_team)

            return redirect(url_for('my_team'))

        return render_template('adicionar_funcionario.html', form=form)

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

