import string
from ..models.barber import BarberUser
from ..models.barber_service import BarberService
from ..models.service import Service
from .. import db


def list_all_services() -> list[Service]:
    query = """
        SELECT DISTINCT * 
        FROM csc535_barber.service;
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
        WHERE Services.`name` = %(name)s;
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
        WHERE BarberServices.`barber_id` = %(user_id)s;
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
            BarberServices.`price`
        FROM csc535_barber.`service` AS Services
        JOIN csc535_barber.`barber_services` AS BarberServices
        ON Services.service_id = BarberServices.service_id
        WHERE BarberServices.barber_id = %(barber_id)s
        AND Services.`service_id` = %(service_id)s  
    """
    results = db.execute(query, {'barber_id': barber_id, 'service_id': service_id})
    if not results:
        return None
    return BarberService(**results[0])


def create_service(name: str):
    query = """
        INSERT INTO csc535_barber.`service` (`service_id`, `name`) 
        VALUES (DEFAULT, %(name)s);      
    """
    db.execute(query, {'name': string.capwords(name)})
    db.commit()
    return retrieve_service(name)


def add_barber_service(barber_id: int, name: str, price: int):
    service = retrieve_service(name)
    query = """
        INSERT INTO csc535_barber.`barber_services` (`service_id`, `barber_id`, `price`) 
        VALUES (%(service_id)s, %(barber_id)s, %(price)s);
    """
    db.execute(query, {
        'barber_id': barber_id, 
        'service': service.id,
        'price': price
    })
    db.execute(query, {'name': string.capwords(name)})
    db.commit()
    return retrieve_barber_service(barber_id, service.id)


def update_barber_service(barber_id: int, service_id: int, price: str):
    query = """
        UPDATE csc535_barber.`service` 
        SET price = %(price)s
        WHERE barber_id = %(barber_id)s
        AND service_id = %(service_id)s
    """
    db.execute(query, {
        'barber_id': barber_id, 
        'service': service_id,
        'price': price
    })
    db.commit()
    return retrieve_barber_service(barber_id, service_id)


def remove_barber_service(barber_id: int, service_id: int):
    query = """
        DELETE FROM csc535_barber.`service` 
        WHERE barber_id = %(barber_id)s
        AND service_id = %(service_id)s
    """
    db.execute(query, {
        'barber_id': barber_id, 
        'service': service_id
    })
    db.commit()
