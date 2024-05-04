from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, RadioField
from wtforms.validators import DataRequired
from ....queries.users import email_exists
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

class Registration(FlaskForm):
    first_name = StringField(
        validators=[
            DataRequired(), 
            Regexp(r'^[a-zA-Z\-\']+$', message='First name must only contain letters, hyphens, and apostrophes.')
        ], 
        label="First Name"
    )

    last_name = StringField(
        validators=[
            DataRequired(), 
            Regexp(r'^[a-zA-Z\-\']+$', message='Last name must only contain letters, hyphens, and apostrophes.')
        ], 
        label="Last Name"
    )

    email = EmailField(
        validators=[DataRequired()], 
        label="Email"
    )

    password = PasswordField(
        validators=[
            DataRequired(),
            Length(min=8, message='Password must be at least 8 characters long.'),
            Regexp(
                r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$', 
                message='Password must include at least one lowercase letter, one uppercase letter, one digit, and one special character.'
            )
        ], 
        label="Password"
    )

    role = RadioField(
        validators=[DataRequired()],
        label="Role",
        choices=[("Barber", "Barber"), ("Client", "Client")]
    )

    submit = SubmitField(label="Register")

    def validate_email(self, field):
            if email_exists(field.data):
                raise ValidationError('This email is already registered. Please use a alternate email.')