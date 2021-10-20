from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, EqualTo

class CreateGoalForm(FlaskForm):
    name = StringField('Nome da meta', validators=[DataRequired()])
    description = StringField('Descrição')
    submit = SubmitField('Criar meta')
