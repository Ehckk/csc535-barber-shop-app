from flask_wtf import FlaskForm
from wtforms import  DateField, TimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RescheduleForm(FlaskForm):
    new_date = DateField('New Date', validators=[DataRequired()], format='%Y-%m-%d')
    new_time = TimeField('New Time', validators=[DataRequired()], format='%H:%M')
    new_duration = IntegerField('New Duration', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Reschedule Appointment")