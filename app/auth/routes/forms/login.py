from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField(
        validators=[DataRequired()], 
        label="Login"
    )
    password = PasswordField(
        validators=[DataRequired()],
        label="Password"
    )
