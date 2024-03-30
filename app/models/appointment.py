from datetime import date, time

from ..queries.users import retrieve_user
from ..utils.date import to_time


HOUR_HEIGHT = 118


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

	def offset(self):
		return to_time(self.start_time).minute // HOUR_HEIGHT
	
	def length(self):
		return self.duration * HOUR_HEIGHT // 60 
	
	def style(self):
		return f"top: {self.offset()}px; min-height: {self.length()}px;"
