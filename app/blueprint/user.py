from flask import Blueprint, render_template
from flask import render_template, flash, redirect, url_for
from app.forms.create_user_form import CreateUserForm
from flask_login import login_required, current_user

from app.controllers.users import *

user = Blueprint('user', __name__, url_prefix='/api/v1')

def init_app(app):