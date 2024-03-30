from flask_wtf import FlaskForm
from wtforms import TextAreaField,  DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class RescheduleAppointmentForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    start_time = TimeField('Start Time', validators=[DataRequired()], format='%H:%M')
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
