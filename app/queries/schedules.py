from datetime import date, time
from typing import Literal
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
    cursor = db.execute(query, {
        "barber_id": barber_id, 
        "start_date": start_date, 
        "interval": interval
    })
    return cursor.fetchall()


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
        "barber": barber_id,
        "weekday_id": weekday_id,
        "start_time": start_time.strftime('%H-%M'),
        "end_time": end_time.strftime('%H-%M')
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
        "start_time": new_start.strftime('%H-%M'),
        "end_time": new_end.strftime('%H-%M')
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
