from collections import OrderedDict, defaultdict
from datetime import date, time
from flask import session

from .window import Window, Interval
from ..utils.date import to_time
from ..utils.email import send_mail
from ..queries.schedules import list_schedule


class User:
    def __init__(
        self, 
        user_id, 
        first_name, 
        last_name, 
        email, 
        role, 
        verified=False
    ):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.verified = verified

    def logout(self):
        session["user"] = None

    def send_reset_email(self):
        send_mail(
            subject="Password Reset", 
            recipients=[self.email], 
            body="""
                You have requested to reset your password.

                ADD LINK HERE
            """
        )

    def reset_password(self, new_password):
        
        return 
    
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

class Client:
    def request_appointment(
        self, 
        barber_id: int, 
        start_date: date,
        start_time: time, 
        duration: int, 
        description=None
    ):
        pass


class Barber:
    def add_availability(
        self, 
        weekday: int, 
        start_time: time, 
        end_time: time
    ):
        pass


class ClientUser(User, Client):
    pass


class BarberUser(User, Barber):
    pass

    def get_schedule(self, current_date: date, interval: str):
        if interval == Interval.MONTH:  # If interval is month, set the date to the first of that month
            current_date = date(current_date.year, current_date.month, 1)

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
        return schedule