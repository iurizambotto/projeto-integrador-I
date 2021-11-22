from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo

class CreateGoalForm(FlaskForm):
    name = StringField('Nome da meta', validators=[DataRequired()])
    description = StringField('Descrição')
    users = SelectMultipleField("Usuários", coerce=int)
    submit = SubmitField('Criar meta')
