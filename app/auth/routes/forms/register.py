from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, RadioField
from wtforms.validators import DataRequired

class Registration(FlaskForm):
    first_name = StringField(
        validators=[DataRequired()], 
        label="First Name"
    )

    last_name = StringField(
        validators=[DataRequired()], 
        label="Last Name"
    )

    email = EmailField(
        validators=[DataRequired()], 
        label="Email"
    )

    password = PasswordField(
        validators=[DataRequired()], 
        label="Password"
    )

    role = RadioField(
        validators=[DataRequired()],
        label="Role",
        choices=["Barber", "Client"]
    )

    submit = SubmitField(label="Register")