from datetime import date, time
from .user import User


class ClientUser(User):
    def request_appointment(
        self, 
        barber_id: int, 
        start_date: date,
        start_time: time, 
        duration: int, 
    ):
        pass