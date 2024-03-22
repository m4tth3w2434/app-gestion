from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField,DateField
from wtforms.validators import DataRequired, Email, Length

from wtforms import BooleanField

class SignupForm(FlaskForm):
    # Campos del formulario con etiquetas y validadores
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Registrar') 

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')
class editForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefono', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    birthdate = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Editar')