from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional


class ServiceForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=32)])
    price = IntegerField("Price", validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Save")
