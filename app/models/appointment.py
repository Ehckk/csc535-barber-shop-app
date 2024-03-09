from datetime import date, time
from .client import ClientUser


class Appointment:
    def __init__(
        self, 
        client: ClientUser, 
        start_date: date, 
        start_time: time, 
        duration: int, 
        is_approved: bool=False
    ):
        self.client = client
        self.start_date = start_date
        self.start_time = start_time
        self.duration = duration
        self.is_approved = is_approved

    def approve(self):
        if not self.is_approved:
            pass


    def cancel(self):
        pass

    def reschedule(
        self, 
        new_date: date,
        new_time: time,
        new_duration: int
    ):
        pass
