from datetime import date, time, timedelta
from collections import defaultdict

from ..models.window import Interval


weekdays = [
    "Sunday", 
    "Monday", 
    "Tuesday", 
    "Wednesday", 
    "Thursday", 
    "Friday", 
    "Saturday"
]


def week_start(current: date):
    return current - timedelta(days=current.weekday())


def month_start(current: date):
    return date(current.year, current.month, 1)


def format_day(start_date: date):
    return start_date.strftime("%B %d, %Y")


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
    Interval.DAY: "calendar_day.html",
    Interval.WEEK: "calendar_week.html",
    Interval.MONTH: "calendar_month.html"  
}

def prev_month_date(current: date):
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
    if units == Interval.WEEK:
        return (
            current - timedelta(weeks=1),
            current + timedelta(weeks=1)
        )
    return (
        current - timedelta(days=1),
        current + timedelta(days=1)
    )


def times_list(units, increment=30):
    if units == Interval.MONTH:
        return None
    
    times = []
    hour = 0
    while hour < 24:
        times.append((time(hour=hour, minute=0), (
            time(hour=hour, minute=0).strftime("%I %p").lstrip("0"),
            time(hour=hour, minute=30).strftime("%I %p").lstrip("0"),
        )))
        hour += 1
    return times


def week_dates(start_date: date, month_bound=False):
    dates = []
    start_month = start_date.month
    current = start_date - timedelta(days=start_date.weekday())
    for _ in range(7):
        if not current.month == start_month and month_bound:
            dates.append(None)
        else:
            current_str = current.strftime("%Y-%b-%d")
            dates.append(current_str)
        current += timedelta(days=1)
    return dates
    

def month_dates(month: int, year: int):
    dates = []
    current = date(year=year, month=month, day=1)
    while current.month == month:
        dates.append(week_dates(current, month_bound=True))
        current += timedelta(weeks=1)
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
    else:
        start = current - timedelta(days=current.weekday())
        end = current + timedelta(days=6)
    return start, end
