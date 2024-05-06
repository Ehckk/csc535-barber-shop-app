import string
from ..models.barber import BarberUser
from ..models.barber_service import BarberService
from ..models.service import Service
from ..models.appointment_service import AppointmentService
from .. import db


def list_all_services() -> list[Service]:
    query = """
        SELECT DISTINCT * 
        FROM csc535_barber.service
        AND deleted = 0;
    """
    results = db.execute(query)
    return [Service(**data) for data in results]


def list_service_barbers(name: str) -> list[BarberUser]:
    query = """
        SELECT 
            Users.`user_id`,
            Users.`first_name`,
            Users.`last_name`,
            Users.`email`,
            Users.`role`,
            Users.`verified`
        FROM csc535_barber.`service` AS Services
        JOIN csc535_barber.`barber_services` AS BarberServices
        ON Services.service_id = BarberServices.service_id
        JOIN csc535_barber.`user` AS Users
        ON BarberServices.barber_id = Users.user_id
        WHERE Services.`name` = %(name)s
        AND deleted = 0;
    """
    results = db.execute(query, {'name': string.capwords(name)})
    return [BarberUser(**data) for data in results]


def list_barber_services(barber_id: int) -> list[BarberService]:
    query = """
        SELECT 
            Services.*,
            BarberServices.`price`
        FROM csc535_barber.`service` AS Services
        JOIN csc535_barber.`barber_services` AS BarberServices
        ON Services.service_id = BarberServices.service_id
        WHERE BarberServices.`barber_id` = %(user_id)s
        AND deleted = 0;
    """
    results = db.execute(query, {'user_id': barber_id})
    return [BarberService(**data) for data in results]


def retrieve_service(name: str) -> Service:
    query = """
        SELECT * 
        FROM csc535_barber.service
        WHERE `name` = %(name)s   
    """
    results = db.execute(query, {'name': string.capwords(name)})
    if not results:
        return create_service(name)
    return Service(**results[0])


def retrieve_barber_service(barber_id: int, service_id: int):
    query = """
        SELECT 
            Services.*,
            BarberServices.`price`,
            BarberServices.description
        FROM csc535_barber.`service` AS Services
        JOIN csc535_barber.`barber_services` AS BarberServices
        ON Services.service_id = BarberServices.service_id
        WHERE BarberServices.barber_id = %(barber_id)s
        AND BarberServices.`service_id` = %(service_id)s
        AND deleted = 0  
    """
    results = db.execute(query, {'barber_id': barber_id, 'service_id': service_id})
    if not results:
        return None
    return BarberService(**results[0])


def retrieve_appointment_services(appointment_id: int):
    query = """
        SELECT 
            Services.*,
            BarberServices.`price`
        FROM csc535_barber.`appointment` AS Appointment
        JOIN csc535_barber.`appointment_services` AS AppointmentServices 
        USING (appointment_id)
        JOIN csc535_barber.`barber_services` AS BarberServices 
        USING (barber_id, service_id)
        JOIN csc535_barber.`service` AS Services
        USING (service_id)
        WHERE Appointment.appointment_id = %(appointment_id)s
        AND deleted = 0
    """
    params = {
        'appointment_id': appointment_id
    }
    results = db.execute(query, params)
    if not results:
        return []
    return [AppointmentService(**data) for data in results]


def create_service(name: str):
    query = """
        INSERT INTO csc535_barber.`service` (`service_id`, `name`) 
        VALUES (DEFAULT, %(name)s);      
    """
    db.execute(query, {'name': string.capwords(name)})
    db.commit()
    return retrieve_service(name)


def add_barber_service(barber_id: int, name: str, price: int, description: str | None=None):
    service = retrieve_service(name)
    if retrieve_barber_service(barber_id, service.id):
        raise AssertionError(f"You already offer a '{name}' service!")
    query = """
        INSERT INTO csc535_barber.`barber_services` (`service_id`, `barber_id`, `price`, `description`, `deleted`) 
        VALUES (%(service_id)s, %(barber_id)s, %(price)s, %(description)s, DEFAULT);
    """
    db.execute(query, {
        'barber_id': barber_id, 
        'service_id': service.id,
        'price': price,
        'description': description or 'DEFAULT'
    })
    db.execute(query, {'name': string.capwords(name)})
    db.commit()
    return retrieve_barber_service(barber_id, service.id)


def update_barber_service(barber_id: int, service_id: int, price: str, description: str | None=None):
    query = """
        UPDATE csc535_barber.`barber_services` 
        SET price = %(price)s, description = %(description)s
        WHERE barber_id = %(barber_id)s
        AND service_id = %(service_id)s
    """
    db.execute(query, {
        'barber_id': barber_id, 
        'service_id': service_id,
        'price': price,
        'description': description
    })
    db.commit()
    return retrieve_barber_service(barber_id, service_id)


def remove_barber_service(barber_id: int, service_id: int):
    query = """
        UPDATE csc535_barber.`barber_services` 
        SET deleted = 1
        WHERE barber_id = %(barber_id)s
        AND service_id = %(service_id)s
    """
    db.execute(query, {
        'barber_id': barber_id, 
        'service_id': service_id
    })
    db.commit()


def add_appointment_service(appointment_id: int, service_id: int):
    query = """
        INSERT INTO csc535_barber.`appointment_services` (`service_id`, `appointment_id`) 
        VALUES (%(service_id)s, %(appointment_id)s);      
    """
    params = {
        "appointment_id": appointment_id,
        "service_id": service_id
    }
    db.execute(query, params)
    db.commit()


def remove_appointment_service(appointment_id: int, service_id: int):
    query = """
        DELETE FROM csc535_barber.`appointment_services` 
        WHERE appointment_id = %(appointment_id)s
        AND service_id = %(service_id)s
    """
    params = {
        "appointment_id": appointment_id,
        "service_id": service_id
    }
    db.execute(query, params)
    db.commit()


def update_appointment_services(appointment_id: int, service_ids: list[int], new_service_ids: list[int]):
    query = """
        DELETE FROM csc535_barber.`appointment_services` 
        WHERE appointment_id = %(appointment_id)s
        AND service_id NOT IN (%(service_ids)s)
    """
    db.execute(query, {
        'appointment_id': appointment_id, 
        'service_ids': ", ".join(map(str, service_ids))
    })
    db.commit()
    for service_id in new_service_ids:

        add_appointment_service(appointment_id, service_id)
