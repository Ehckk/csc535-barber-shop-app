from datetime import date
from flask_wtf import FlaskForm
from wtforms import DateField, SelectMultipleField, TimeField, IntegerField, SelectField, SubmitField
from wtforms.widgets import CheckboxInput
from wtforms.validators import DataRequired, NumberRange
from ....queries import services, users
from ....utils.form import get_choices


def get_barber_choices():
    barbers = users.list_barbers()
    choices = list(map(
        lambda barber: (barber.id, barber.display_name()), 
        barbers
    ))
    return get_choices(choices)


def get_service_choices(barber_id: int):
    barber_services = services.list_barber_services(barber_id)
    choices = list(map(
        lambda service: (service.id, str(service)), 
        barber_services
    ))
    return choices


class RequestBarberForm(FlaskForm):
    barber = SelectField(choices=get_barber_choices(), validators=[DataRequired()])


class RequestDateForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField(label="Next")


class RequestForm(RequestBarberForm, RequestDateForm):
    pass


class RequestAppointmentForm(FlaskForm):
    services = SelectMultipleField(label="Services")
    start_time = TimeField('Start Time', validators=[DataRequired()], format='%H:%M')
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    cancel = SubmitField(label="Back")
    submit = SubmitField(label="Book")
    