from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class EditGoalForm(FlaskForm):
    name = StringField('Nome da meta', validators=[DataRequired()])
    description = StringField('Descrição', validators=[DataRequired()])
    users = SelectMultipleField("Usuários", coerce=int)
    achieved = SelectField("Concluída?", coerce=int)
    submit = SubmitField('Editar meta')
