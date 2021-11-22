from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo

class CreateNewRelationshipForm(FlaskForm):
    user_id = SelectField("Usuário", coerce=int)
    submit = SubmitField('Adicionar usuário ao time')
