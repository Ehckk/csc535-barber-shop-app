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

HOUR_HEIGHT = 118

		
class Window:
	def __init__(self, start_time: time, end_time: time):
		self.start_time = start_time
		self.end_time = end_time
	