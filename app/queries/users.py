from typing import Literal
from .. import db

def check_email(email: str):
    query = """
        SELECT `user_id` 
        FROM csc535_barber.`user`
        WHERE `email` = %(email)s 
    """    
    cursor = db.execute(query, {"email": email})
    return cursor.fetchone()


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
    cursor = db.execute(query, {"email": email, "password": password})
    return cursor.fetchone()


def list_barbers():
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
    cursor = db.execute(query)
    return cursor.fetchall()


def retrieve_user(id: int):
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
    cursor = db.execute(query, {"id": id})
    return cursor.fetchone()    


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
