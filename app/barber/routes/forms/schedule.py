from flask_wtf import FlaskForm
from wtforms import TimeField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ScheduleForm(FlaskForm):
    weekday = SelectField(label="Weekday", choices=[(0,"Monday"),(1,"Tuesday"),(2,"Wednesday"),(3,"Thursday"),(4,"Friday"),(5,"Saturday"),(6,"Sunday")], validators=[DataRequired()])
    start_time = TimeField(label="Start Time", validators=[DataRequired()])
    end_time = TimeField(label="End Time", validators=[DataRequired()])
    submit = SubmitField(label="Save Availability")