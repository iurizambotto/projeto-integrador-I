from datetime import datetime
from wtforms.fields.simple import PasswordField
from app.extensions.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    achieved = db.Column(db.Boolean())
    achieved_at = db.Column(db.DateTime())

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'),
        nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    achieved = db.Column(db.Boolean())
    achieved_at = db.Column(db.DateTime())

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(150), nullable=False, unique=True)
    age = db.Column(db.Integer())
    authenticated = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self) -> str:
        return self.format()

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'age': self.age or None
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

