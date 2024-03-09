from typing import Literal
from .. import db

def check_email(email: str):
    query = """
        SELECT * 
        FROM csc535_barber.`user`
        WHERE `email` = %(email)s 
    """    
    cursor = db.execute(query, {"email": email})
    return cursor.fetchone()


def check_password(email: str, password: str):
    query = """
        SELECT * 
        FROM csc535_barber.`user`
        WHERE `email` = %(email)s 
        AND `password` = %(password)s
    """
    cursor = db.execute(query, {"email": email, "password": password})
    return cursor.fetchone()


def list_barbers():
    query = """
        SELECT * 
        FROM csc535_barber.`user`
        WHERE `role` = 'Barber'
    """
    cursor = db.execute(query)
    return cursor.fetchall()


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
            %(password)s, 
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
