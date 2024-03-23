from datetime import date, time, timedelta
from collections import defaultdict

from ..models.window import Interval


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


def times_list(increment=30):
    times = []
    hour = 0
    while hour < 24:
        times.append((time(hour=hour, minute=0), (
            time(hour=hour, minute=0).strftime("%I %p").lstrip("0"),
            time(hour=hour, minute=30).strftime("%I %p").lstrip("0"),
        )))
        hour += 1
    print(times)
    return times