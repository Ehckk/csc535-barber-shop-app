from flask_wtf import FlaskForm
from wtforms import  TextAreaField, IntegerField, StringField
from wtforms.validators import DataRequired

class ServicesForm(FlaskForm):
    name =  StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])