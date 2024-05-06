from datetime import date

from ..models.barber_service import BarberService
from ..models.window import Window
from .date import to_time


def get_services_table(barber_services: list[BarberService]):
    services = list(map(lambda s: [s.name], barber_services))
    prices = list(map(lambda s: [f"${s.price}"], barber_services))
    data = list(zip(services, prices))
    return data


def get_schedule_table(barber_schedule: list[dict]):
    weekday_ids = set()
    day_names = []
    availability_windows = []
    day_availability = []
    for schedule in barber_schedule:
        weekday_id = schedule["weekday_id"]
        if weekday_id not in weekday_ids: # Must be unique
            weekday_ids.add(weekday_id)
            day_names.append([schedule["day_name"]])
            if day_availability:
                availability_windows.append(day_availability)
                day_availability = []

        start_time = to_time(schedule["start_time"])
        end_time = to_time(schedule["end_time"])
        window = Window(start_time, end_time)
        day_availability.append(window)
    availability_windows.append(day_availability)
    data = list(zip(day_names, availability_windows))
    return data


def get_unavailable_table(unavailable_dates: list[dict[str, date]], ranges=True):
    start_dates = list(map(lambda s: [s['start_date']], unavailable_dates))
    if not ranges:
        return list(zip(start_dates))
    end_dates = list(map(lambda s: [s['end_date']], unavailable_dates))
    data = list(zip(start_dates, end_dates))
    return data


def get_appointments_table(appointments: list):
    data = list(zip(map(lambda appt: (str(appt),), appointments)))
    return data