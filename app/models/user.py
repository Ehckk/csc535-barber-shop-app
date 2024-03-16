from collections import OrderedDict
from datetime import date, time
from flask import session

from .window import Window, Interval
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
