from datetime import date, time

from ..models.appointment import Appointment
from .. import db


def list_appointments(appointments_data):
    appointments = []
    for appointment_data in appointments_data:
        appointment = Appointment(**appointment_data)
        appointments.append(appointment)
    return appointments


def list_barber_appointments(barber_id: int):
    query = """
        SELECT * 
        FROM csc535_barber.`appointment` 
        WHERE `barber_id` = %(barber_id)s;
    """
    cursor = db.execute(query, {"barber_id": barber_id})
    return list_appointments(cursor.fetchall())


def list_client_appointments(client_id: int):
    query = """
        SELECT * 
        FROM csc535_barber.`appointment`
        WHERE `client_id` = %(client_id)s;
    """
    cursor = db.execute(query, {"client_id": client_id})
    return list_appointments(cursor.fetchall())


def retrieve_appointment(appointment_id: int): 
    query = """
        SELECT * 
        FROM csc535_barber.`appointment` 
        WHERE `appointment_id` = %(appointment_id)s;
    """
    cursor = db.execute(query, {"appointment_id": appointment_id})
    appointment_data = cursor.fetchone()
    return Appointment(**appointment_data)


def create_appointment(
    barber_id: int,
    client_id: int,
    start_date: date,
    start_time: time,
    duration: int
):
    query = """
        INSERT INTO csc535_barber.`appointment` VALUES (
            DEFAULT, 
            %(barber_id)s, 
            %(client_id)s, 
            %(start_date)s, 
            %(start_time)s, 
            %(duration)s, 
            DEFAULT, 
            DEFAULT
        );
    """
    db.execute(query, {
        "barber_id": barber_id,
        "client_id": client_id,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "start_time": start_time.strftime('%H-%M'),
        "duration": duration
    })
    db.commit()



def approve_appointment(appointment_id: int):
    query = """
        UPDATE csc535_barber.`appointment` 
        SET `is_approved` = 1
        WHERE `appointment_id` = %(appointment_id)s;
    """
    db.execute(query, {"appointment_id": appointment_id})
    db.commit()


def update_appointment(
    appointment_id: int,
    new_date: date,
    new_time: time,
    new_duration: int
):
    query = """
        UPDATE csc535_barber.`appointment` 
        SET `booked_date` = %(new_date)s, 
            `start_time` = %(new_time)s,
            `duration` = %(new_duration)s
        WHERE `appointment_id` = %(appointment_id)s;
    """
    db.execute(query, {
        "new_date": new_date.strftime('%Y-%m-%d'),
        "new_time": new_time.strftime('%H-%M'),
        "new_duration": new_duration,
        "appointment_id": appointment_id
    })
    db.commit()


def delete_appointment(appointment_id: int):
    query = """
        DELETE FROM csc535_barber.`appointment` 
        WHERE `appointment_id` = %(appointment_id)s;
    """
    db.execute(query, {"appointment_id": appointment_id})
    db.commit()
