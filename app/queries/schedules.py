from datetime import date, datetime, time, timedelta
from typing import Literal

from ..utils.date import to_time
from ..models.window import Window
from .. import db


def list_schedule(
    barber_id: int, 
    start_date: date, 
    interval: Literal['M', 'W', 'D']
):
    query = """
        CALL csc535_barber.`sp_barber_availability_for_range`(
            %(barber_id)s, 
            %(start_date)s, 
            %(interval)s
        );
    """
    results = db.execute(query, {
        "barber_id": int(barber_id), 
        "start_date": str(start_date), 
        "interval": interval
    })
    return results


def create_schedule(
    weekday_id: int,
    barber_id: int,
    start_time: time,
    end_time: time
):
    query = """
        INSERT INTO csc535_barber.`schedule` VALUES (
            DEFAULT, 
            %(barber_id)s, 
            %(weekday_id)s, 
            %(start_time)s, 
            %(end_time)s
        );
    """
    db.execute(query, {
        "barber_id": barber_id,
        "weekday_id": weekday_id,
        "start_time": start_time.strftime('%H:%M'),
        "end_time": end_time.strftime('%H:%M')
    })
    db.commit()
    

def update_schedule(
    schedule_id: int,
    new_start: time,
    new_end: time 
):
    query = """
        UPDATE csc535_barber.`schedule` 
        SET `start_time` = %(start_time)s,
            `end_time` = %(end_time)s
        WHERE `schedule_id` = %(schedule_id)s;
    """
    db.execute(query, {
        "schedule_id": schedule_id,
        "start_time": new_start.strftime('%H:%M'),
        "end_time": new_end.strftime('%H:%M')
    })
    db.commit()
 

def delete_schedule(
    schedule_id: int
):
    query = """
        DELETE FROM csc535_barber.`schedule` 
        WHERE `schedule_id` = %(schedule_id)s;
    """
    db.execute(query, {"schedule_id": schedule_id})
    db.commit()


def is_available_for_date(barber_id: int, target_date=date):
    query = """
        CALL sp_barber_availability_for_range(
            %(barber_id)s,
            %(target_date)s,
            'D'
        )
    """
    result = db.execute(query, {
        "barber_id": barber_id,
        "target_date": target_date.strftime("%Y-%m-%d")
    })
    return len(result) > 0


def schedule_for_date(barber_id: int, target_date=date):
    params = {
        "barber_id": barber_id,
        "target_date": target_date.strftime("%Y-%m-%d")
    }
    query = """
        SELECT * 
        FROM csc535_barber.`vw_barber_availability`
        WHERE `booked_date` = %(target_date)s
        AND `barber_id` = %(barber_id)s
    """
    results = db.execute(query, params)
    if not results:
        query = """
            SELECT * 
            FROM csc535_barber.`vw_barber_availability`
            WHERE weekday_id = WEEKDAY(%(target_date)s)
            AND `barber_id` = %(barber_id)s
            AND `booked_date` IS NULL
        """
        results = db.execute(query, params)
    availability = []
    for row in results:
        start_time = to_time(row["start_time"])
        end_time = to_time(row["end_time"])
        window = Window(start_time, end_time)
        availability.append(window) 
    return availability
