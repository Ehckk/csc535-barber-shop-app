from datetime import date, datetime, timedelta

from ..models.barber import BarberUser
from ..models.appointment import Appointment
from ..queries import appointments
from ..utils.date import to_time


def create_if_valid(
    barber: BarberUser,
    client_id: int, 
    start_date: date, 
    start_time: timedelta, 
    duration: int, 
    services: list[int]
):
    start_datetime = datetime.combine(start_date, to_time(start_time))
    if start_datetime < datetime.now():
        raise AssertionError("Appointment must be in the future!") 
    Appointment.validate_appointnment(
        barber_name=barber.display_name(),
        barber_id=barber.id,
        start_date=start_date,
        start_time=start_time,
        duration=duration,
        services=services
    )
    appointment = appointments.create_appointment(
        barber_id=barber.id,
        client_id=client_id,
        start_date=start_date,
        start_time=to_time(start_time),
        duration=duration
    )
    # TODO services