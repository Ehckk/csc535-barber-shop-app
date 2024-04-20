from ..models.user import BarberUser, ClientUser, User
from .. import db
from werkzeug.security import generate_password_hash

def update_user_password(email: str, new_password: str):
    hashed_password = generate_password_hash(new_password)
    query = "UPDATE user SET `password` = %s WHERE `email` = %s;"
    with db.connection.cursor() as cursor:
        cursor.execute(query, (hashed_password, email))
        db.connection.commit()