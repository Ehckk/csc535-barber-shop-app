from datetime import date, time
from ..queries.users import retrieve_user


class Appointment:
    def __init__(
        self, 
        appointment_id: int,
        client_id: int,
        barber_id: int,
        description: str,
        booked_date: date, 
        start_time: time, 
        duration: int, 
        is_approved: bool=False
    ):
        self.id = appointment_id
        self.client = retrieve_user(client_id)
        self.barber = retrieve_user(barber_id)
        self.description = description
        self.booked_date = booked_date
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
