from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.validators import DataRequired


class UnavailableForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
