from datetime import date, time
from ..models.appointment import Appointment
from .. import db


def list_appointments(appointments_data) -> list[Appointment]:
    appointments = []
    for appointment_data in appointments_data:
        appointment = Appointment(**appointment_data)
        appointments.append(appointment)
    return appointments


def appointments_for_date(barber_id: int, target_date: date):
    query = """
        SELECT * 
        FROM csc535_barber.`appointment` 
        WHERE `barber_id` = %(barber_id)s
        AND `booked_date` = %(target_date)s
        AND `is_approved` = 1
        ORDER BY `booked_date`, `start_time`;
    """
    results = db.execute(query, {
        "barber_id": barber_id,
        "target_date": target_date
    })
    return list_appointments(results)


def appointments_between_dates(barber_id: int, start: date, end: date):
    query = """
        SELECT * 
        FROM csc535_barber.`appointment` 
        WHERE `barber_id` = %(barber_id)s
        AND `booked_date` >= %(start)s
        AND `booked_date` <= %(end)s
        AND `is_approved` = 1
        ORDER BY `booked_date`, `start_time`;
    """
    results = db.execute(query, {
        "barber_id": barber_id,
        "start": start,
        "end": end
    })
    return list_appointments(results)


def list_barber_appointments(barber_id: int, booked: bool=True, prev: bool=False):
    query = """
        SELECT * 
        FROM csc535_barber.`appointment` 
        WHERE `barber_id` = %(barber_id)s
        AND `is_approved` = %(booked)s
        AND (NOW() > TIMESTAMP(`booked_date`, `start_time`)) = %(is_prev)s;
    """
    results = db.execute(query, {
        "barber_id": barber_id,
        "booked": booked,
        "is_prev": 1 if prev else 0
    })
    return list_appointments(results)


def list_barber_history(barber_id: int):
    current_date = date.today().isoformat()
    
    query = """
        SELECT * 
        FROM csc535_barber.`appointment` 
        WHERE `barber_id` = %(barber_id)s AND `booked_date` < %(current_date)s;
    """
    results = db.execute(query, {"barber_id": barber_id, "current_date": current_date})
    return list_appointments(results)



def list_client_appointments(client_id: int, is_booked: bool=True, prev: bool=False):
    is_booked = 1 if is_booked else 0
    is_prev = 1 if prev else 0
    params = {
        "client_id": client_id,
        "is_booked": is_booked,
        "is_prev": is_prev
    }
    query = """
        SELECT *
        FROM csc535_barber.`appointment`
        WHERE `client_id` = %(client_id)s
        AND `is_approved` = %(is_booked)s
        AND (NOW() > TIMESTAMP(`booked_date`, `start_time`)) = %(is_prev)s
    """
    results = db.execute(query, params)
    return list_appointments(results)
  

def list_client_history(barber_id: int):
    current_date = date.today().isoformat()
    
    query = """
        SELECT * 
        FROM csc535_barber.`appointment` 
        WHERE `client_id` = %(client_id)s AND `booked_date` < %(current_date)s;
    """
    results = db.execute(query, {"client_id": barber_id, "current_date": current_date})
    return list_appointments(results)


def retrieve_appointment(appointment_id: int): 
    query = """
        SELECT * 
        FROM csc535_barber.`appointment` 
        WHERE `appointment_id` = %(appointment_id)s;
    """
    results = db.execute(query, {"appointment_id": appointment_id})
    if not results:
        return None
    appointment_data = results[0] 
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
            DEFAULT
        );
    """
    db.execute(query, {
        "barber_id": barber_id,
        "client_id": client_id,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "start_time": start_time.strftime('%H:%M'),
        "duration": duration
    })
    db.commit()
    query = """
        SELECT * FROM csc535_barber.`appointment`
        WHERE barber_id = %(barber_id)s
        AND client_id = %(client_id)s
        AND booked_date = %(start_date)s 
        AND start_time = %(start_time)s
        AND duration = %(duration)s
        AND is_approved = 0
    """
    results = db.execute(query, {
        "barber_id": barber_id,
        "client_id": client_id,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "start_time": start_time.strftime('%H:%M'),
        "duration": duration
    })
    return Appointment(**results[0])


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
        "new_time": new_time.strftime('%H:%M'),
        "new_duration": new_duration,
        "appointment_id": appointment_id
    })
    db.commit()
    return retrieve_appointment(appointment_id)


def delete_appointment(appointment_id: int):
    query = """
        DELETE FROM csc535_barber.`appointment` 
        WHERE `appointment_id` = %(appointment_id)s;
    """
    db.execute(query, {"appointment_id": appointment_id})
    db.commit()


def retrieve_conflicting(appointment: Appointment, is_booked=False):
    booked_date = appointment.booked_date
    start_time = appointment.start_time
    end_time = appointment.end_time()
    is_booked = '1' if is_booked else '0'
    query = """
        SELECT * FROM csc535_barber.`appointment`
        WHERE `is_approved` = %(is_booked)s 
        AND `barber_id` = %(barber_id)s
        AND NOT `appointment_id` = %(appointment_id)s
        AND `booked_date` = %(booked_date)s
        AND (
            (`start_time` >= %(start_time)s AND `start_time` < %(end_time)s) 
            OR (
                DATE_ADD(`start_time`, INTERVAL `duration` MINUTE) >= %(start_time)s
                AND DATE_ADD(`start_time`, INTERVAL `duration` MINUTE) < %(end_time)s
            )
        )    
    """
    results = db.execute(query, {
        "is_booked": is_booked,
        "appointment_id": appointment.id,
        "barber_id": appointment.barber.id,
        "booked_date": booked_date,
        "start_time": start_time,
        "end_time": end_time,
    })
    return list_appointments(results)


def cancel_prev_unbooked():
    query = """
        DELETE FROM csc535_barber.`appointment` 
        WHERE `is_approved` = 0
        AND NOW() < TIMESTAMP(`booked_date`, `start_time`);
    """
    db.execute(query)
    db.commit()