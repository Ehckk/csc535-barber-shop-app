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
    return
    

def update_schedule(
    schedule_id: int,
    new_start: time,
    new_end: time    
):
    return
    

def delete_schedule(
    schedule_id: int
):
    return
