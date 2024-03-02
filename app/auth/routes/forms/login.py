from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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
    submit = SubmitField(label="Log In")
