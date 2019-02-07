from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )


class RegisterForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )
