from datetime import date, timedelta
from collections import defaultdict

from ..models.window import Interval


def todays_date(interval: int, prev: bool):
    today = date.today()
    if prev:
        return today - timedelta(days=interval)
    return today + timedelta(days=interval)


def week_start(interval: int, prev: bool):
    today = date.today()
    start_date = today - timedelta(days=today.weekday())
    if prev:
        return start_date - timedelta(weeks=interval)
    return start_date + timedelta(weeks=interval)


def month_start(interval: int, prev: bool):
    today = date.today()
    start_date = date(today.year, today.month, 1)
    if prev:
        return start_date - timedelta(months=interval)
    return start_date + timedelta(months=interval)


base_dates = defaultdict(lambda: date.today(), {
    Interval.DAY: todays_date,
    Interval.WEEK: week_start,
    Interval.MONTH: month_start
})


def format_day(start_date: date):
    return start_date.strftime("%B %-d, %Y")


def format_month_day(start_date: date):
    return start_date.strftime("%B %-d")


def format_week(start_date: date):
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


date_names = defaultdict(format_day, {
    Interval.DAY: format_day,
    Interval.WEEK: format_week,
    Interval.MONTH: format_month
})
