from collections import OrderedDict, defaultdict
from datetime import date, time

from .user import User
from .window import Interval, Window
from ..queries.schedules import list_schedule, schedule_for_date
# from ..queries.appointments import create_appointment
from ..utils.date import to_time, date_window


class BarberUser(User):
    def add_availability(self, weekday: int, start_time: time, end_time: time):
        pass
    
    def get_schedule(self, current_date: date, interval: str):
        current_date, _ = date_window(current_date, interval)
        windows = list_schedule(self.id, current_date, interval)  # List of dates and time slots
        schedule = defaultdict(OrderedDict)  # Use them to create a dictionary 

        for window in windows:
            schedule_date: str = window["date"].strftime("%Y-%m-%d")  # Key: date
            start_time = to_time(window["start_time"])
            time_key = str(time(hour=start_time.hour, minute=(start_time.minute // 30) * 30))
            if not schedule.get(time_key, None):
                schedule[schedule_date][time_key] = []  # Value: list of time slots for that date  
            schedule[schedule_date][time_key].append(
                Window(
                    start_time=start_time, 
                    end_time=to_time(window["end_time"])
                )
            )
        print(list(map(str, schedule.get('2024-05-07', {}).get('12:00:00', []))))
        return schedule
        

    def __str__(self) -> str:
        return self.display_name()