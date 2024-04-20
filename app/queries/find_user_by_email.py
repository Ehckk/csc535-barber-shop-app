from ..models.user import BarberUser, ClientUser, User
from .. import db

def find_user_by_email(email: str):
    query = "SELECT `user_id`, `email`, `first_name`, `last_name`, `role`, `verified` FROM user WHERE `email` = %s;"
    with db.connection.cursor() as cursor:
        cursor.execute(query, (email,))
        return cursor.fetchone()