from typing import Literal

from ..models.user import BarberUser, ClientUser, User
from .. import db

def check_email(email: str):
    query = """
        SELECT `user_id` 
        FROM csc535_barber.`user`
        WHERE `email` = %(email)s 
    """    
    results = db.execute(query, {"email": email})
    if not results:
        return None
    return results[0] 


def check_password(email: str, password: str):
    query = """
        SELECT 
            `user_id`,
            `email`,
            `role`
        FROM csc535_barber.`user`
        WHERE `email` = %(email)s 
        AND `password` = SHA(%(password)s)
    """
    results = db.execute(query, {"email": email, "password": password})
    if not results:
        return None
    return results[0] 



def list_barbers() -> list[BarberUser]:
    query = """
        SELECT 
            `user_id`,
            `first_name`,
            `last_name`,
            `email`,
            `role`,
            `verified`
        FROM csc535_barber.`user`
        WHERE `role` = 'Barber'
    """
    results = db.execute(query)
    if not results:
        return []
    barbers = []
    for barber_data in results:
        barber = BarberUser(**barber_data)
        barbers.append(barber)
    return barbers


def retrieve_user(id: int) -> User:
    query = """
        SELECT 
            `user_id`,
            `first_name`,
            `last_name`,
            `email`,
            `role`,
            `verified`
        FROM csc535_barber.`user`
        WHERE `user_id` = %(id)s
    """
    results = db.execute(query, {"id": id})
    if results is None:
        return None
    user_data = results[0]
    if user_data["role"] == "Barber":
        return BarberUser(**user_data)
    return ClientUser(**user_data)


def create_user(
    email: str, 
    password: str, 
    first_name: str,
    last_name: str,
    role: Literal['Client', 'Barber']
):
    query = """
        INSERT INTO csc535_barber.`user` VALUES (
            DEFAULT, 
            %(email)s, 
            SHA(%(password)s), 
            %(first_name)s, 
            %(last_name)s,
            %(role)s,
            DEFAULT
        );
    """
    db.execute(query, {
        "email": email,
        "password": password,
        "first_name": first_name, 
        "last_name": last_name, 
        "role": role
    })
    db.commit()
    result = check_email(email)
    return result["user_id"]

def verify_email(user_id):
    query = """
        UPDATE csc535_barber.user
        SET verified = 1
        WHERE user_id = %(user_id)s
    """
    db.execute(query, {"user_id": user_id})
    db.commit()
