from flask_wtf import FlaskForm
from wtforms import SelectField, TimeField, SubmitField
from wtforms.validators import DataRequired

class BarberScheduleForm(FlaskForm):
    weekday_choices = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]
    
    weekday = SelectField(
        'Weekday', 
        choices=weekday_choices, 
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    start_time = TimeField(
        'Start Time', 
        validators=[DataRequired()], 
        format='%H:%M',
        render_kw={"class": "form-control", "type": "time"}
    )
    end_time = TimeField(
        'End Time', 
        validators=[DataRequired()], 
        format='%H:%M',
        render_kw={"class": "form-control", "type": "time"}
    )
    submit = SubmitField(
        'Submit Schedule',
        render_kw={"class": "btn btn-primary"}
    )
