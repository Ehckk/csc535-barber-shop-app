from datetime import datetime
from .user import User

class Client:
    def request_appointment(self, barber_id: int, start: datetime, duration: int, description=None):
        pass

class ClientUser(User, Client):
    def __init__(self, *args, **kwargs):
        super(User).__init__(*args, **kwargs)
