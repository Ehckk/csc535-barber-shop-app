from .user import User
from .window import Window, Interval
from ..queries.schedules import list_schedule
from datetime import date, time
from collections import OrderedDict


class Barber:
    def add_availability(
        self, 
        weekday: int, 
        start_time: time, 
        end_time: time
    ):
        pass


class BarberUser(User, Barber):
    def __init__(self, *args, **kwargs):
        super(User).__init__(*args, **kwargs)

    def get_schedule(self, start_date: date, interval: Interval):
        if interval == Interval.MONTH:  # If interval is month, set the date to the first of that month
            start_date = date(start_date.year, start_date.month, 1)

        windows = list_schedule(self.id, start_date, interval.value)  # List of dates and time slots
        schedule: OrderedDict[str, list[Window]] = OrderedDict()  # Use them to create a dictionary 

        for window in windows:  
            schedule_date: str = window["date"]  # Key: date
            if not schedule.get(schedule_date, None):
                schedule[schedule_date] = []  # Value: list of time slots for that date
                
            schedule_window = Window(
                start_time=window["start_time"],
                end_time = window["end_time"]
            )
            schedule[schedule_date].append(schedule_window)
        return schedule 
