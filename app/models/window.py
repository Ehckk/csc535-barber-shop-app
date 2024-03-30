from datetime import time
from enum import StrEnum


class Interval(StrEnum):
	DAY 	= 'D'
	WEEK    = 'W'
	MONTH   = 'M'


weekdays = {
	"Mon": 0,
	"Tue": 1,
	"Wed": 2,
	"Thu": 3,
	"Fri": 4,
	"Sat": 5,
	"Sun": 6
}

HOUR_HEIGHT = 59

		
class Window:
	def __init__(self, start_time: time, end_time: time):
		self.start_time = start_time
		self.end_time = end_time
	
	def offset(self):
		return self.start_time.minute // HOUR_HEIGHT
	
	def length(self):
		start = (self.start_time.hour * 60) + self.start_time.minute
		end = (self.end_time.hour * 60) + self.end_time.minute
		return (end - start) * HOUR_HEIGHT // 60 
	
	def style(self):
		return f"top: {self.offset()}px; min-height: {self.length()}px;"
