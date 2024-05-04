from .. import db
import logging
logging.basicConfig(level=logging.DEBUG)

from hashlib import sha1  

def hash_password_sha1(password: str) -> str:
    hashed_password = sha1(password.encode()).hexdigest()
    return hashed_password

def update_user_password(email: str, new_password: str):
    logging.debug("Updating password for email: %s", email)
    logging.debug("New password: %s", new_password)
    
    hashed_password = hash_password_sha1(new_password)
    
    query = "UPDATE user SET password = %s WHERE email = %s;"
    with db.connection.cursor() as cursor:
        cursor.execute(query, (hashed_password, email))
        db.connection.commit()

