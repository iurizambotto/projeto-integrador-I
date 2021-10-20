from flask import Blueprint, render_template
from flask.helpers import url_for
from app.forms.login_form import LoginForm
# from app.extensions.database import db
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.forms.login_form import LoginForm

from app.controllers.users import *

login = Blueprint('index', __name__)

def init_app(app):