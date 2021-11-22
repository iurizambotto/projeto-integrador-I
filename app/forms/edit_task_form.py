from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class EditTaskForm(FlaskForm):
    name = StringField('Nome da atividade', validators=[DataRequired()])
    description = TextAreaField('Descrição')
    user_id = SelectField("Responsável", coerce=int)
    achieved = SelectField("Concluído?", coerce=int)
    goal_id = SelectField("Meta relacionada", coerce=int)
    submit = SubmitField('Criar atividade')
