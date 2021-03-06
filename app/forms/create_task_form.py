from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo

class CreateTaskForm(FlaskForm):
    name = StringField('Nome da atividade', validators=[DataRequired()])
    description = TextAreaField('Descrição')
    user_id = SelectField("Responsável", coerce=int)
    goal_id = SelectField("Responsável", coerce=int)
    submit = SubmitField('Criar atividade')
