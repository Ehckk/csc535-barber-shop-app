from datetime import date, timedelta, time

from .window import Window
from ..queries.schedules import schedule_for_date
from ..queries.users import retrieve_user
from ..utils.date import to_time


def validate_appointment_time(
    availability: list[Window], 
    start_time: timedelta, 
    duration: int
):
    for window in availability:
        if window.is_between(start_time, duration):
            return True
    return False


HOUR_HEIGHT = 118


class Appointment:
	def __init__(
		self, 
		appointment_id: int,
		client_id: int,
		barber_id: int,
		booked_date: date, 
		start_time: timedelta, 
		duration: int, 
		is_approved: bool=False
	):
		self.id = appointment_id
		self.client = retrieve_user(client_id)
		self.barber = retrieve_user(barber_id)
		self.booked_date = booked_date
		self.start_time = to_time(start_time)
		self.duration = duration
		self.is_approved = is_approved

	def end_time(self):
		return to_time(
			timedelta(
				hours=self.start_time.hour, 
				minutes=self.start_time.minute + self.duration
			)
		)

	def offset(self):
		return self.start_time.minute // HOUR_HEIGHT
	
	def length(self):
		return self.duration * HOUR_HEIGHT // 60 
	
	def style(self):
		return f"top: {self.offset()}px; min-height: {self.length()}px;"

	def time_range(self):
		end_time = self.end_time()
		if (self.start_time.hour < 12) == (end_time.hour < 12):
			start = self.start_time.strftime('%I:%M')
			end = end_time.strftime('%I:%M')
			return f"{start} - {end} {end_time.strftime('%p')}"
		start = self.start_time.strftime('%I:%M %p')
		end = end_time.strftime('%I:%M %p')
		return f"{start} - {end}"
	
	@staticmethod
	def validate_appointnment(
			barber_name: str,
			barber_id: int,
			start_date: date, 
			start_time: timedelta, 
			duration: int, 
			services: list[int]
		):
		availability = schedule_for_date(barber_id, start_date)
		if len(services) == 0:
			message = "Select at least one service!"
			raise AssertionError(message) 
		if not validate_appointment_time(availability, start_time, duration):
			message = f"{barber_name} is unavailable during this time"
			raise AssertionError(message) 

	def __str__(self):
		return f"{self.booked_date.strftime('%b %d, %Y')} @ {self.time_range()}"