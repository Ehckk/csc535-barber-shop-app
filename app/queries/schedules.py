from datetime import date, time
from typing import Literal

from ..utils.date import to_time
from ..models.window import Window
from .. import db

TIME_FORMAT = '%H:%M:%S'


def barber_weekly_schedule(barber_id: int):
    query = """
        SELECT 
            W.*,
            S.`start_time`,
            S.`end_time`
        FROM csc535_barber.`schedule` AS S
        JOIN csc535_barber.`weekday` AS W
        USING (`weekday_id`)
        WHERE `barber_id` = %(barber_id)s
        ORDER BY S.`weekday_id`, S.`start_time`, S.`end_time`
    """
    return db.execute(query, {"barber_id": barber_id})


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


def check_existing(
    weekday_id: int,
    barber_id: int,
    start_time: time,
    end_time: time
):
    query = """
        SELECT schedule_id
        FROM csc535_barber.schedule
        WHERE barber_id = %(barber_id)s
        AND weekday_id = %(weekday_id)s
        AND %(start_time)s BETWEEN start_time AND end_time 
        AND %(end_time)s BETWEEN start_time AND end_time
    """
    results = db.execute(query, {
        "barber_id": int(barber_id), 
        "weekday_id": int(weekday_id),
        "start_time": start_time.strftime(TIME_FORMAT),
        "end_time": end_time.strftime(TIME_FORMAT)
    }) or []
    exists = len(results) > 0
    return exists


def check_overlapping(
    weekday_id: int,
    barber_id: int,
    start_time: time,
    end_time: time
):
    query = """
        SELECT 
            *,
            MIN(start_time) OVER () AS min_start_time,
            MAX(end_time) OVER () AS max_end_time
        FROM csc535_barber.schedule
        WHERE barber_id = %(barber_id)s AND weekday_id = %(weekday_id)s
        AND (
            start_time BETWEEN %(start_time)s AND %(end_time)s OR
            end_time BETWEEN %(start_time)s AND %(end_time)s
        )
        ORDER BY schedule_id
    """

    overlapping = db.execute(query, {
        "barber_id": int(barber_id), 
        "weekday_id": int(weekday_id),
        "start_time": start_time.strftime(TIME_FORMAT),
        "end_time": end_time.strftime(TIME_FORMAT)
    })
    if len(overlapping) > 0:
        first_overlapping = overlapping[0]
        update_schedule(
            schedule_id=first_overlapping["schedule_id"],
            new_start=min(to_time(first_overlapping["min_start_time"]), start_time),
            new_end=max(to_time(first_overlapping["max_end_time"]), end_time)
        )
        if len(overlapping) > 1:
            remaining_ids = list(map(lambda s: s["schedule_id"], overlapping[1:]))
            for schedule_id in remaining_ids:
                delete_schedule(schedule_id)
        return False
    return True


def create_schedule(
    weekday_id: int,
    barber_id: int,
    start_time: time,
    end_time: time
):
    if not check_overlapping(weekday_id, barber_id, start_time, end_time):
        return
    
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
        "start_time": start_time.strftime(TIME_FORMAT),
        "end_time": end_time.strftime(TIME_FORMAT)
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
        "start_time": new_start.strftime(TIME_FORMAT),
        "end_time": new_end.strftime(TIME_FORMAT)
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
