from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField(
        validators=[DataRequired()], 
        label="Email"
    )
    password = PasswordField(
        validators=[DataRequired()],
        label="Password"
    )
    submit = SubmitField(label="Log In")
