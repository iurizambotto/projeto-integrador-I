from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
# from wtforms.fields.core import RadioField
from wtforms.validators import DataRequired, EqualTo

required_message = "Esse campo é obrigatório"

class CreateUserForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(required_message)])
    password = PasswordField('Senha', validators=[DataRequired(required_message)])
    confirm_password = PasswordField('Confirme a Senha', validators=[DataRequired(required_message), EqualTo("password", message="As senhas não são iguais.")])
    name = StringField('Nome', validators=[DataRequired(required_message)])
    role = StringField('Cargo')
    function = RadioField('Função', choices=[(0, 'Funcionário'), (1, 'Gerente')], validators=[DataRequired(required_message)])
    submit = SubmitField('Criar')
