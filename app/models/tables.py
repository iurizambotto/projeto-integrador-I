from datetime import datetime
from enum import unique
from wtforms.fields.simple import PasswordField
from app.extensions.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    achieved = db.Column(db.Boolean())
    achieved_at = db.Column(db.DateTime(), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'),
        nullable=True)
    achieved = db.Column(db.Boolean())
    achieved_at = db.Column(db.DateTime())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())  

    def __repr__(self) -> str:
        return self.format()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'goal_id': self.goal_id or None,
            'achieved': self.achieved or False,
            'achieved_at': self.achieved_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'created_by': self.created_by,
        }

class UsersGoals(db.Model):
    __tablename__ = 'users_goals'
    
    __table_args__ = (
        db.UniqueConstraint(
            'user_id',
            'goal_id',
            name='pk_user_goal',
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'),
        nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

class UsersTeams(db.Model):
    __tablename__ = 'users_team'
    
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'),
    nullable=False, unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(128))
    email = db.Column(db.String(150), nullable=False, unique=True)
    role = db.Column(db.String(150), nullable=True)
    function = db.Column(db.String(20), nullable=True)
    authenticated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self) -> str:
        return self.format()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role or None,
            'function': self.function or None
        }

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

