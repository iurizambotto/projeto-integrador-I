from flask import Flask

from app.extensions import (
    configuration,
    database,
    auth,
    admin,
)
from app.blueprint import views

app = Flask(__name__)
configuration.init_app(app)
database.init_app(app)
views.init_app(app)
auth.init_app(app)
admin.init_app(app)

