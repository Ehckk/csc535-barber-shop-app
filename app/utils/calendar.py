from collections import defaultdict, OrderedDict
from datetime import time, timedelta

from ..models.window import Window 
from .date import (
    date_window,
    Interval,
)
from ..queries.appointments import appointments_between_dates, appointments_for_date


def calendar_appointments(barber_id, current_date, interval):
    if interval == Interval.DAY:
        appointment_data = appointments_for_date(barber_id, current_date)
    else:
        start, end = date_window(current_date, interval)
        appointment_data = appointments_between_dates(barber_id, start, end)
    appointments = defaultdict(OrderedDict)

    for appointment in appointment_data:
        booked_date: str = appointment.booked_date.strftime("%Y-%m-%d")  # Key: date
        start_time = appointment.start_time
        time_key = str(time(hour=start_time.hour, minute=(start_time.minute // 30) * 30))
        if not appointments.get(time_key, None):
            appointments[booked_date][time_key] = []
        appointments[booked_date][time_key].append(appointment)
    return appointments


def validate_appointment_time(
    availability: list[Window], 
    start_time: timedelta, 
    duration: int
):
    for window in availability:
        if window.is_between(start_time, duration):
            return True
    return False
