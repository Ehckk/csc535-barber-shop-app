from datetime import date, datetime, time, timedelta
from collections import defaultdict

from ..models.window import Interval


weekdays = [
    "Monday", 
    "Tuesday", 
    "Wednesday", 
    "Thursday", 
    "Friday", 
    "Saturday",
    "Sunday"
]


def week_start(current: date):
    return current - timedelta(days=current.weekday())


def month_start(current: date):
    return date(current.year, current.month, 1)


def format_day(start_date: date):
    return start_date.strftime("%A, %B %d, %Y")


def format_month_day(start_date: date):
    return start_date.strftime("%B %d")


def format_week(current: date):
    start_date = current - timedelta(days=current.weekday())
    end_date = start_date + timedelta(days=6)

    if not end_date.year == start_date.year:
        return f"{format_day(start_date)} - {format_day(end_date)}"

    year = start_date.strftime("%Y")
    if not start_date.month == end_date.month:
        return f"{format_month_day(start_date)} - {format_month_day(end_date)}, {year}"
    
    month = start_date.strftime("%B")
    return f"{month} {start_date.day}-{end_date.day}, {year}"


def format_month(start_date: date):
    return start_date.strftime("%B %Y")


interval_values = set([v.value for v in Interval])


date_names = defaultdict(format_day, {
    Interval.DAY: format_day,
    Interval.WEEK: format_week,
    Interval.MONTH: format_month
})


date_templates = {
    Interval.DAY: "calendar_day_{}.html",
    Interval.WEEK: "calendar_week_{}.html",
    Interval.MONTH: "calendar_month_{}.html"  
}

def prev_month_date(current: date):
    if current.month == date.today().month:
        return None
    prev_month = current.month - 1
    if prev_month == 0:
        return date(current.year - 1, 12, 1)
    return date(current.year, prev_month, 1)


def next_month_date(current: date):
    next_month = current.month + 1
    if next_month > 12:
        return date(current.year + 1, 1, 1)
    return date(current.year, next_month, 1)


def date_increments(current: date, units):
    if units == Interval.MONTH:
        return (
            prev_month_date(current),
            next_month_date(current)
        )
    today = date.today()
    if units == Interval.WEEK:
        prev_week = current - timedelta(weeks=1)
        next_week = current + timedelta(weeks=1)
        if prev_week < today - timedelta(days=today.weekday()):
            prev_week = None
        return prev_week, next_week 
    prev_day = current - timedelta(days=1)
    next_day = current + timedelta(days=1)
    if prev_day < date.today():
        prev_day = None
    return prev_day, next_day


def times_list(schedule, appointments):
    all_times = set()
    for schedule_time in schedule.values():
        for key in schedule_time.keys():
            all_times.add(key)
    for appointment_time in appointments.values():
        for key in appointment_time.keys():
            all_times.add(key)
    if not len(all_times) == 0:
        min_hour = int(min(all_times).split(":")[0])
    else:
        min_hour = 0
    times = []
    hour = min_hour
    while hour < 24:
        hour_times = (str(time(hour=hour, minute=0)), str(time(hour=hour, minute=30)))
        times.append((time(hour=hour, minute=0).strftime("%I %p").lstrip("0"), hour_times))
        hour += 1
    return times


def week_dates(start_date: date, month=None):
    dates = []
    start_month = month or start_date.month
    current = start_date - timedelta(days=start_date.weekday())
    for _ in range(7):
        if not current.month == start_month and month:
            dates.append(None)
        else:
            dates.append(current)
        current += timedelta(days=1)
    return dates
    

def month_dates(month: int, year: int):
    dates = []
    current = date(year=year, month=month, day=1)
    week = week_dates(current, month=month)
    while any([d.month == month for d in week if d is not None]):
        dates.append(week)
        current += timedelta(weeks=1)
        week = week_dates(current, month=month)
    return dates


def dates_list(current: date, units):
    if units == Interval.MONTH:
        return month_dates(current.month, current.year)
    if units == Interval.WEEK:
        return week_dates(current)
    return None


def date_window(current: date, units):
    if units == Interval.MONTH:
        start = date(current.year, current.month, 1)
        end = next_month_date(current) - timedelta(days=1)
    elif units == Interval.WEEK:
        start = current - timedelta(days=current.weekday())
        end = current + timedelta(days=6)
    else:
        start = current
        end = None
    return start, end


def to_time(value: timedelta):
    return (datetime.min + value).time()
